// ai_spotibot_player
// AudioMIX
// main.cpp

#include <iostream>
#include <vector>
#include <portaudio.h>
#include <thread>
#include <chrono>
#include <cstring>
#include <atomic>
#include <string>
#include <mutex>

#include "main.h"

// DSP Core + Modules
#include "audio/dsp/core/dsp_chain.h"
#include "audio/dsp/modules/digital_choir.h"
#include "audio/dsp/modules/shimmer.h"
#include "audio/dsp/modules/null_sink.h"
#include "audio/dsp/core/eq_params.h"
#include "audio/dsp/core/eq_params_parse.h"
#include "audio/dsp/modules/eq_module.h"

using namespace audiomix::dsp;

// does not parse full JSON yet (no extra deps)
// string match for recognized commands and stash raw payload lines for later
// TODO: replace the string matching with a real JSON parser; deserialize into EQparams
struct ControlBus {
    // Pointer to the EQ module inside DSP chain
    audiomix::dsp::EqModule* eq = nullptr;

    // latest raw EQ command line received
    // control thread writes under mutex; audio thread copies when signaled
    std::mutex pendingMutex;
    audiomix::dsp::EqParams pendingEqParams;
    std::atomic<bool> hasPendingEqParams{false};

    std::atomic<bool> running{true};
};

static inline bool containsCmd(const std::string& line, const char* cmd) {
    // simple match for: "cmd":"<cmd>"
    const std::string needle = std::string("\"cmd\":\"") + cmd + "\"";
    return line.find(needle) != std::string::npos;
}

static void controlLoop(ControlBus* bus) {
    std::string line;
    while (bus->running.load(std::memory_order_relaxed) && std::getline(std::cin, line)) {
        if (line.empty()) continue;

        if (containsCmd(line, "ping")) {
            std::cout << "{\"cmd\":\"pong\"}" << std::endl;
            continue;
        }

        audiomix::dsp::EqParams parsed;
        if (!audiomix::dsp::parseEqSetLine(line, parsed)) {
            // parse JSON
            std::cout << "{\"cmd\":\"error\",\"error\":\"bad_eq_payload\"}" << std::endl;
            continue;
        }

        // Apply EQ from the control thread (off audio thread)
        // EQModule is responsible for publishing coeff updates to audio thread (safely)
        if (bus->eq) {
            bus->eq->setParams(parsed, 10.0f);    // smooth ms
        }

        {
            std::lock_guard<std::mutex> lock(bus->pendingMutex);
            bus->pendingEqParams = parsed;
        }
        bus->hasPendingEqParams.store(true, std::memory_order_release);
        // ack instead of silence (for testing purposes)
        std::cout << "{\"cmd\":\"ack\",\"ack\":\"eq.set\"}" << std::endl;
        continue;

        // unknown command
        std::cout << "{\"cmd\":\"error\",\"error\":\"unknown_command\"}" << std::endl;
    }
}

// AudioState - holds the DSP chain and temporary buffers
struct AudioState {
    DspChain chain;
    double sampleRate = 44100.0;      // 44.1 kHz
    unsigned int maxBlockSize = 512;  // 512 samples max buffer size

    // reference EQ module ptr
    audiomix::dsp::EqModule* eq = nullptr;

    // control plane hook
    ControlBus* control = nullptr;

    // store last params
    audiomix::dsp::EqParams lastEqParams{};
    bool hasEqParams = false;

    std::vector<float> inL, inR;
    std::vector<float> outL, outR;
};

// PortAudio Callback
static int audioCallback(const void* inputBuffer,
                         void* outputBuffer,
                         unsigned long framesPerBuffer,
                         const PaStreamCallbackTimeInfo*,
                         PaStreamCallbackFlags,
                         void* userData)
{
    auto* state = static_cast<AudioState*>(userData);

    const float* in = static_cast<const float*>(inputBuffer);
    float* out      = static_cast<float*>(outputBuffer);

    // Process through the DSP chain
    // stereo wrapper - internally uses processMulti
    state->chain.process(state->inL.data(), state->inR.data(),
                         state->outL.data(), state->outR.data(),
                         static_cast<unsigned int>(framesPerBuffer));

    // Interleave stereo output
    for (unsigned long i = 0; i < framesPerBuffer; ++i) {
        out[2 * i + 0] = state->outL[i];
        out[2 * i + 1] = state->outR[i];
    }

    return paContinue;
}

// Main
int main(int argc, char* argv[])
{
    std::cout << "AudioMIX DSP is running!" << std::endl;

    // start control-plane listener (NDJSON over stdin)
    // runs in parallel with audio engine
    // TODO: message will actually alter DSP
    ControlBus control;
    std::thread controlThread(controlLoop, &control);
    controlThread.detach();

    bool headlessMode = false;
    PaStream* stream = nullptr;

    // original audio init calls
    for (int i = 1; i < argc; ++i) {
        if (std::string(argv[i]) == "--headless") {
            headlessMode = true;
        }
    }

    // Set up AudioState + DSP chain
    AudioState state;
    state.sampleRate = 44100.0;
    state.maxBlockSize = 512;
    state.control = &control;

    state.chain.setSampleRate(state.sampleRate);
    state.chain.setMaxBlockSize(state.maxBlockSize);

    // Add DSP modules
    // Digital Choir
    auto* choir = state.chain.emplaceModule<DigitalChoirModule>(8);
    choir->setParameter("wet", 0.8f);
    choir->setParameter("spread", 1.0f);

    // Shimmer - can process "chorused" audio
    auto* shimmer = state.chain.emplaceModule<ShimmerModule>();
    shimmer->setParameter("wet", 0.4f);          // overall mix
    shimmer->setParameter("feedback", 0.7f);     // tail length
    shimmer->setParameter("octave_mix", 1.0f);   // full shimmer strength
    shimmer->setParameter("delay_ms", 550.0f);   // tail pre-delay

    // EQ module
    auto* eq = state.chain.emplaceModule<audiomix::dsp::EqModule>();
    state.eq = eq;
    control.eq = eq;

    // Headless mode (hardware agnostic)
    if (headlessMode) {
        // adds sinks BEFORE prepare() so sinks get prepare/reset correctly
        state.chain.emplaceModule<audiomix::dsp::NullSink>();
    }

    state.chain.prepare();

    if (!headlessMode) {
        PaStreamParameters inputParams{};
        PaStreamParameters outputParams{};

        // initialize PortAudio via main_utils.cpp
        if (!initializeAudio()) {
            return 1;
        }

        // PortAudio Stream setup
        PaDeviceIndex inDev = Pa_GetDefaultInputDevice();
        PaDeviceIndex outDev = Pa_GetDefaultOutputDevice();

        if (outDev == paNoDevice) {
            std::cerr << "No default output device found.\n";
            std::cerr << "Available devices:\n";
            list_audio_devices();
            shutdownAudio();
            return 1;
        }

        const PaDeviceInfo* outInfo = Pa_GetDeviceInfo(outDev);
        if (!outInfo) {
            std::cerr << "Output device info is null.\n";
            std::cerr << "Available devices:\n";
            list_audio_devices();
            shutdownAudio();
            return 1;
        }

        // output is req
        outputParams.device = outDev;
        outputParams.channelCount = 2;
        outputParams.sampleFormat = paFloat32;
        outputParams.suggestedLatency =
            outInfo->defaultLowOutputLatency;

        // input is optional: if missing, pass nullptr and callback will receive
        PaStreamParameters* inParamsPtr = nullptr;
        if (inDev != paNoDevice) {
            const PaDeviceInfo* inInfo = Pa_GetDeviceInfo(inDev);
            if (inInfo) {
                inputParams.device = inDev;
                inputParams.channelCount = 2;
                inputParams.sampleFormat = paFloat32;
                inputParams.suggestedLatency = inInfo->defaultLowInputLatency;
                inParamsPtr = &inputParams;
            } else {
                std::cerr << "Warn: input device info is null; continuing output-only.\n";
            }
        } else {
            std::cerr << "Warn: no default input device; continuing output-only.\n";
        }

        PaError err = Pa_OpenStream(&stream,
                      inParamsPtr,
                      &outputParams,
                      state.sampleRate,
                      state.maxBlockSize,
                      paNoFlag,
                      audioCallback,
                      &state);

        if (err != paNoError) {
            std::cerr << "Err: Pa_OpenStream failed: " << Pa_GetErrorText(err) << "\n";
            std::cerr << "Available devices:\n";
            list_audio_devices();
            shutdownAudio();
            return 1;
        }

        err = Pa_StartStream(stream);
        if (err != paNoError) {
            std::cerr << "Err: Pa_StartStream failed: " << Pa_GetErrorText(err) << "\n";
            Pa_CloseStream(stream);
            shutdownAudio();
            return 1;
        }

        std::cout << "Audio stream running. Press Ctrl+C to exit.\n";
    }

    // Simple run loop (for now)
    // future AudioMIX loop will go here
    if (!headlessMode) {
        while (Pa_IsStreamActive(stream) == 1) {
            Pa_Sleep(100);
        }

        Pa_StopStream(stream);
        Pa_CloseStream(stream);
        shutdownAudio();
    } else {
        // Headless run loop (no PortAudio)
        while (true) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }
}
