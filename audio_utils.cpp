#include <iostream>
#include <portaudio.h>

extern "C" void list_audio_devices() {
    Pa_Initialize();
    int numDevices = Pa_GetDeviceCount();
    for (int i = 0; i < numDevices; i++) {
        const PaDeviceInfo *deviceInfo = Pa_GetDeviceInfo(i);
        std::cout << "Device" << i << ": " << deviceInfo->name << std :: endl;
    }
    Pa_Terminate();
}