# Minimum required version
cmake_minimum_required(VERSION 3.10)
project(AI_SPOTIBOT_PLAYER LANGUAGES C CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set compilers
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)

# Find PortAudio
find_path(PORTAUDIO_INCLUDE_DIR portaudio.h 
    PATHS "/usr/include" "/usr/local/include" "${CMAKE_SOURCE_DIR}/portaudio/include"
)
 
find_library(PORTAUDIO_LIBRARY portaudio 
    PATHS "/usr/lib/x86_64-linux-gnu" "/usr/local/lib" "${CMAKE_SOURCE_DIR}/portaudio/build/libportaudio.a"
)

if(PORTAUDIO_INCLUDE_DIR AND PORTAUDIO_LIBRARY)
    message(STATUS "PortAudio found: Includes at ${PORTAUDIO_INCLUDE_DIR}, Library at ${PORTAUDIO_LIBRARY}")
    include_directories(${PORTAUDIO_INCLUDE_DIR})
else()
    message(FATAL_ERROR "PortAudio not found! Check installation.")
endif()

# Include project directory
include_directories(${CMAKE_SOURCE_DIR})

# Set source files
set(SOURCES main.cpp)

# Define executables
add_executable(spotibot_exec ${SOURCES})

# Link PortAudio and system audio dependencies
target_link_libraries(spotibot_exec 
    PRIVATE 
        ${PORTAUDIO_LIBRARY}
        asound #ALSA
        jack # JACK Audio Connection Kit
        pthread # Required by PortAudio
        m # Math library
)

