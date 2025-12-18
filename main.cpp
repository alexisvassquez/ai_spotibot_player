// ai_spotibot_player
// AudioMIX
// main.cpp

#include <iostream>
#include <vector>
#include <portaudio.h>
#include <thread>
#include <chrono>

#include "main.h"

// DSP Core + Modules
#include "audio/dsp/core/dsp_chain.h"
#include "audio/dsp/modules/digital_choir.h"
#include "audio/dsp/modules/shimmer.h"
#include "audio/dsp/modules/null_sink.h"

using namespace audiomix::dsp;

// AudioState - holds the DSP chain and temporary buffers
struct AudioState {
    DspChain chain;
    double sampleRate = 44100.0;
    unsigned int maxBlockSize = 512;

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

    // Resize temp buffers
    state->inL.resize(framesPerBuffer);
    state->inR.resize(framesPerBuffer);
    state->outL.resize(framesPerBuffer);
    state->outR.resize(framesPerBuffer);

    // De-interleave input to L/R
    if (in) {
        for (unsigned long i = 0; i < framesPerBuffer; ++i) {
            state->inL[i] = in[2 * i + 0];
            state->inR[i] = in[2 * i + 1];
        }
    } else {
        std::fill(state->inL.begin(), state->inL.end(), 0.0f);
        std::fill(state->inR.begin(), state->inR.end(), 0.0f);
    }

    // Process through the DSP chain
    state->chain.process(state->inL.data(), state->inR.data(),
                         state->outL.data(), state->outR.data(),
                         static_cast<unsigned int>(framesPerBuffer));

    // Interleave back to output
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

    state.chain.prepare();

    // Headless mode (hardware agnostic)
    if (headlessMode) {
        state.chain.emplaceModule<audiomix::dsp::NullSink>();
    } else {
        // PortAudio Stream setup
        PaStreamParameters inputParams{};
        PaStreamParameters outputParams{};

        inputParams.device = Pa_GetDefaultInputDevice();
        inputParams.channelCount = 2;
        inputParams.sampleFormat = paFloat32;
        inputParams.suggestedLatency =
            Pa_GetDeviceInfo(inputParams.device)->defaultLowInputLatency;

        outputParams.device = Pa_GetDefaultOutputDevice();
        outputParams.channelCount = 2;
        outputParams.sampleFormat = paFloat32;
        outputParams.suggestedLatency =
            Pa_GetDeviceInfo(outputParams.device)->defaultLowOutputLatency;

        Pa_OpenStream(&stream,
                      &inputParams,
                      &outputParams,
                      state.sampleRate,
                      state.maxBlockSize,
                      paNoFlag,
                      audioCallback,
                      &state);

        Pa_StartStream(stream);

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
