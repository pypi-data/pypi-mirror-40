cmake_minimum_required(VERSION 3.10.0)

set(CMAKE_COLOR_MAKEFILE ON)

# enable_testing()

if (DURANGO OR ORBIS OR ANDROID OR LINUX)
	unset(WIN32)
	unset(WIN64)
endif()

# Either Win32 or Win64
if (WIN32)
    include("${CMAKE_SOURCE_DIR}/cmake_files/platforms/windows.cmake")
else()
    include("${CMAKE_SOURCE_DIR}/cmake_files/platforms/linux.cmake")
endif()

# if (${PLATFORM} STREQUAL "Win64" OR ${PLATFORM} STREQUAL "Win32")
#     set(RUNTIME_LIBRARY_SUFFIX "dll")
#     set(STATICLIBRARY_SUFFIX = "lib")
# elseif(${PLATFORM} STREQUAL "Linux" OR ${PLATFORM} STREQUAL "Mac")
#     set(RUNTIME_LIBRARY_SUFFIX "so")
#     set(STATICLIBRARY_SUFFIX "a")
# endif()