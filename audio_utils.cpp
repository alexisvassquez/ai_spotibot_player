#include <iostream>
#include <portaudio.h>
#include "audio_utils.h"

bool initializeAudio() {
    PaError err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "PortAudio initialization failed: " << Pa_GetErrorText(err) << std::end;
        return false;
    }
    std::cout << "PortAudio initialized successfully!" << std::end;
    return true;
}

void shutdownAudio() {
    Pa_Terminate();
    std::cout << "PortAudio terminated." << std::end;
}

extern "C" void list_audio_devices() {
    Pa_Initialize();
    int numDevices = Pa_GetDeviceCount();
    for (int i = 0; i < numDevices; i++) {
        const PaDeviceInfo *deviceInfo = Pa_GetDeviceInfo(i);
        std::cout << "Device" << i << ": " << deviceInfo->name << std :: endl;
    }
    Pa_Terminate();
}
