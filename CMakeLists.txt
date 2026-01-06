# ai_spotibot_player
# AudioMIX
# CMakeLists.txt

# Minimum required version
cmake_minimum_required(VERSION 3.10)
project(AudioMIX LANGUAGES C CXX)

# ------------------------------
# General Build Settings
# ------------------------------
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_VERBOSE_MAKEFILE OFF)

# ------------------------------
# File & Directory Structure
# ------------------------------
# Add include paths
include_directories(
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/audio
    ${CMAKE_SOURCE_DIR}/audio/dsp
    ${CMAKE_SOURCE_DIR}/audio/dsp/core
    ${CMAKE_SOURCE_DIR}/audio/dsp/modules
)

# Collect Source Files (SAFE)
file(GLOB_RECURSE PROJECT_SOURCES
    "${CMAKE_SOURCE_DIR}/*.cpp"
    "${CMAKE_SOURCE_DIR}/audio/*.cpp"
    "${CMAKE_SOURCE_DIR}/audio/*/*.cpp"
    "${CMAKE_SOURCE_DIR}/audio/*/*/*.cpp"
)
list(APPEND PROJECT_SOURCES ${CMAKE_SOURCE_DIR}/main_utils.cpp)

# ------------------------------
# EXCLUDE
# ------------------------------
# Python envs and other unwanted directories
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "myenv/")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "venv/")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "env/")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "amenv/")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "__pycache__")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "site-packages")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "dist-packages")

# CMake internal folders
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "CMakeFiles/")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "CMakeScripts/")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "CompilerIdC")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "CompilerIdCXX")

# Jupyter notebook checkpoints
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "ipynb_checkpoints")

# build/ directory (where build artifacts live)
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "/build/")

# PortAudio examples
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "portaudio/")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "portaudio/src")
list(FILTER PROJECT_SOURCES EXCLUDE REGEX "portaudio/examples")

message(STATUS "Filtered project source files:")
foreach(src ${PROJECT_SOURCES})
    message(STATUS " ${src}")
endforeach()

# ------------------------------
# PortAudio Detection
# ------------------------------
find_path(PORTAUDIO_INCLUDE_DIR portaudio.h
    PATHS "/usr/include" "/usr/local/include" "${CMAKE_SOURCE_DIR}/portaudio/include"
)

find_library(PORTAUDIO_LIBRARY portaudio
    PATHS "/usr/lib/x86_64-linux-gnu" "/usr/local/lib" "${CMAKE_SOURCE_DIR}/portaudio/build/libportaudio.a"
)

if(PORTAUDIO_INCLUDE_DIR AND PORTAUDIO_LIBRARY)
    message(STATUS "PortAudio found!")
    message(STATUS " Includes: ${PORTAUDIO_INCLUDE_DIR}")
    message(STATUS " Library: ${PORTAUDIO_LIBRARY}")
    include_directories(${PORTAUDIO_INCLUDE_DIR})
else()
    message(FATAL_ERROR "PortAudio not found! Did you install libportaudio-dev?")
endif()

# ------------------------------
# Core DSP / Engine Targets
# ------------------------------
file(GLOB DSP_CORE_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/audio/dsp/core/*.cpp"
    "${CMAKE_SOURCE_DIR}/audio/dsp/core/*.cc"
    "${CMAKE_SOURCE_DIR}/audio/dsp/core/*.cxx"
)

file(GLOB DSP_CORE_HEADERS CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/audio/dsp/core/*.h"
    "${CMAKE_SOURCE_DIR}/audio/dsp/core/*.hpp"
)

if (DSP_CORE_SOURCES)
    add_library(audiomix_dsp_core STATIC ${DSP_CORE_SOURCES} ${DSP_CORE_HEADERS})
else()
    add_library(audiomix_dsp_core INTERFACE)
endif()

target_include_directories(audiomix_dsp_core INTERFACE
    ${CMAKE_SOURCE_DIR}
)

# ------------------------------
# DSP Modules
# ------------------------------
add_subdirectory(audio/dsp/modules)

# ------------------------------
# Build Executable
# ------------------------------
add_executable(audiomix ${PROJECT_SOURCES})

# ------------------------------
# Link Libraries
# ------------------------------
target_link_libraries(audiomix
    PRIVATE
        audiomix_dsp_core
        audiomix_dsp_modules
        ${PORTAUDIO_LIBRARY}
        asound        # ALSA
        jack          # JACK
        pthread       # PortAudio requirement
        m             # Math lib
)
