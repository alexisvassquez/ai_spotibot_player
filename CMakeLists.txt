# Specify 'gcc' CXXCompilerID.
# set(CMAKE_MODULE_PATH).
# find_library(portaudio.h REQUIRED)
# set("portaudio.h"/${LIBRARY_DIR_PATH}).
# set(SOURCE_DIR_PATH="/home/wholesomedegenerate/ai_spotibot_player")
# set(BUILD_DIR_PATH="/home/wholesomedegenerate/ai_spotibot_player/build")

# Minimum required version
cmake_minimum_required(VERSION 3.25.1)
project(<AI_SPOTIBOT_PLAYER> LANGUAGES C CXX)
set(CMAKE_VERBOSE_MAKEFILE ON)

# C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Sets PREFIX PATHS
set(CMAKE_PREFIX_PATH "/home/wholesomedegenerate/portaudio" ${CMAKE_PREFIX_PATH})

# Set CMAKE_SOURCE_DIR and CMAKE_BUILD_DIR
set(SOURCE_DIR="/home/wholesomedegenerate/ai_spotibot_player")

# Set compiler
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)

# set module path
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "/home/wholesomedegenerate/portaudio/cmake/modules/FindPulseAudio.cmake")

# Find PortAudio
find_path(PORTAUDIO_INCLUDE_DIR portaudio PATHS "/home/wholesomedegenerate/portaudio/include")
find_library(PORTAUDIO_LIBRARY portaudio PATHS "${/usr/lib/x86_64-linux-gnu}/libportaudio.so;${/usr/lib/x86_64-linux-gnu}/libportaudiocpp.so;${/home/wholesomedegenerate}/portaudio")

set(PORTAUDIO_LIB_DIR "/home/wholesomedegenerate/portaudio")
set(PORTAUDIO_INCLUDE_DIR "/home/wholesomedegenerate/portaudio/include")

include_directories(${PORTAUDIO_INCLUDE_DIR})
link_directories(${PORTAUDIO_LIB_DIR})

if(NOT PORTAUDIO_INCLUDE_DIR OR NOT PORTAUDIO_LIBRARY)
        message(FATAL_ERROR "PortAudio not found!")
endif()

# Source files
file(GLOB SOURCES "${SOURCE_DIR}/*.cpp")
set(SOURCES
	"main.cpp"
)
set(PORTAUDIO_SOURCES 
	"${/usr/include}/portaudio.h"
	"${/usr/lib/x86_64-linux-gnu}/libportaudio.so"
	"${SOURCE_DIR}/audio_utils.cpp"
	"${/home/wholesomedegenerate}/portaudio/src/os/pa_unix_util.c"
	"/pa_unix_util.h"
)

add_library(portaudio STATIC ${PORTAUDIO_SOURCES})

# Executables
add_executable(audio_utils.cpp ${CMAKE_SOURCE_DIR})
add_executable(ai_spotibot_player ${SOURCES})

# Sets paths to libraries 
set(ARROW_LIBRARY_PATH_SUFFIXES
        "/usr"
        "/usr/local"
        "/usr/include"
        "/usr/lib"
        "/lib/python3.11"
        "/python3.11/site-packages"
        "/site-packages/cmake_modules"
        "/site-packages/pyarrow"
        "/usr/config/pulse"
        "/usr/myenv"
        "/myenv/lib"
        "/myenv/lib/python3.11/site-packages"
        "/site-packages/pyaudio"
 	"/myenv/lib64"
        "/lib64/python3.11/site-packages"
        "/lib64/python3.11/site-packages/pyaudio"
        "/usr/lib/x86_64-linux-gnu"
	"/home/wholesomedegenerate/portaudio"
)

set(ARROW_INCLUDE_PATH_SUFFIXES
        "include"
        "lib"
        "Library"
        "Library/include"
        "lib64"
)

set(ADD_THIRDPARTY_LIB
        "/usr"
        "/usr/local"
 	"/myenv/lib64"
        "/lib64/python3.11/site-packages"
        "/lib64/python3.11/site-packages/pyaudio"
        "/usr/lib/x86_64-linux-gnu"
)

include_directories(${ARROW_INCLUDE_PATH_SUFFIXES})
include_directories("/home/wholesomedegenerate/portaudio/include")
link_directories(${ARROW_LIBRARY_PATH_SUFFIXES})
link_directories("/usr/lib")

