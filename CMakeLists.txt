#include ${portaudio.h}
#include ${"mnt/c/Users/alexi/Downloads/pa_stable_v190700_20210406/portaudio/cmake_support/portaudioTargets.cmake"}

cmake_minimum_required(VERSION 3.10)
project(<SPOTIFY_ROBOT>)
set(CMAKE_MODULE_PATH "")
find_package(portaudio.h REQUIRED)

add_executable(portaudioTargets audio_utils.cpp)
target_link_libraries(portaudioTargets portaudio::portaudio)
