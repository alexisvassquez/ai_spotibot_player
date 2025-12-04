#pragma once

// Include necessary libraries
#include <portaudio.h>
#include <iostream>

// Audio initialization / Device helpers

// Initialize PortAudio
bool initializeAudio();

// Shut down PortAudio
void shutdownAudio();

// List audio devices (C-callable)
extern "C" void list_audio_devices();

// DSP Chain Struct (forward declaration)
// Allows main.cpp to use AudioState before it's fully defined
struct AudioState;

