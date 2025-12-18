// ai_spotibot_player
// AudioMIX
// main_utils.cpp

// Replaces old audio_utils.cpp

#include "main.h"

// Initialize PortAudio
bool initializeAudio() {
    PaError err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "PortAudio initialization failed: "
                 << Pa_GetErrorText(err) << std::endl;
        return false;
    }

    std::cout << "PortAudio initialized successfully!" << std::endl;
    return true;
}

// Shut down PortAudio
void shutdownAudio() {
    Pa_Terminate();
    std::cout << "PortAudio shutdown completed." << std::endl;
}

// List audio devices
extern "C" void list_audio_devices() {
    int numDevices = Pa_GetDeviceCount();
    if (numDevices < 0) {
        std::cerr << "Pa_GetDeviceCount error:\n";
        return;
    }

    for (int i = 0; i < numDevices; ++i) {
        const PaDeviceInfo* info = Pa_GetDeviceInfo(i);
        if (!info) {
            std::cerr << "Device " << i << ": <null>\n";
            continue;
        }

        std::cout << "Device " << i << ": " << info->name << "\n";
    }
}
