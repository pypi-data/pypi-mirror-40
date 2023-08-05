cmake_minimum_required(VERSION 3.10.0)

set_property(GLOBAL PROPERTY USE_FOLDERS On)

if (CMAKE_CL_64 OR ${CMAKE_GENERATOR} MATCHES "Win64")
    #64bit
    set(BUILD_CPU_ARCHITECTURE x64)
    set(PLATFORM "win64")
else()
    #32it
    set(BUILD_CPU_ARCHITECTURE x86)
    set(PLATFORM "win32")
endif()

set(CMAKE_CODELITE_USE_TARGETS Off)

if (MSVC_VERSION LESS 1900)
    message(FATAL_ERROR "Visual Studio need 2017.")
endif()

if (NOT CMAKE_VS_MSBUILD_COMMAND)
    message(FATAL_ERROR "Not exits msbuild.exe.")
endif()

function(__build_project)
    set(MSBUILD_EXE "${CMAKE_VS_MSBUILD_COMMAND}")
    set(PROJECT_FILE_PATH "${${PROJECT_NAME}_BINARY_DIR}/${PROJECT_NAME}.sln")
    execute_process(
        COMMAND
            ${MSBUILD_EXE} /nologo
            ${PROJECT_FILE_PATH}
        RESULT_VARIABLE
            RESULT_CODE
    )
    if (${RESULT_CODE} EQUAL 1)
        message(FATAL_ERROR "MSBUILD error!!!")
        return()
    endif()
endfunction()

add_definitions(-DPLATFORM_WINDOWS=1)

set(STATIC_LIBRARY_SUFFIX "lib")
set(RUNTIME_LIBRARY_SUFFIX "dll")
set(LINK_LIBRARY_SUFFIX "lib")
