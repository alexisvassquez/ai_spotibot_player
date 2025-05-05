#ifndef AUDIO_UTILS_H
#define AUDIO_UTILS_H

// Include necessary libraries
#include <portaudio.h>
#include <iostream>

// Function declarations
bool initializeAudio();
void shutdownAudio();
extern "C" void list_audio_devices();

#endif // AUDIO_UTILS_H
