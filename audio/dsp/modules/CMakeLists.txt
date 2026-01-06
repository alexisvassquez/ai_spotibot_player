# ai_spotibot_player
# AudioMIX
# audio/dsp/modules/CMakeLists.txt

file(GLOB CONFIGURE_DEPENDS DSP_MODULE_SOURCES
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cc"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cxx"
)

file(GLOB CONFIGURE_DEPENDS DSP_MODULE_HEADERS
    "${CMAKE_CURRENT_SOURCE_DIR}/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.hpp"
)

message(STATUS "DSP module sources: ${DSP_MODULE_SOURCES}")

add_library(audiomix_dsp_modules STATIC
    ${DSP_MODULE_SOURCES}
    ${DSP_MODULE_HEADERS}
)

target_include_directories(audiomix_dsp_modules PUBLIC
    ${CMAKE_SOURCE_DIR}
)

target_link_libraries(audiomix_dsp_modules PUBLIC
    audiomix_dsp_core
)
