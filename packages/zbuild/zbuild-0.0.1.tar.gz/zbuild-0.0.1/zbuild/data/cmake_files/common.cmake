cmake_minimum_required(VERSION 3.10.0)

function(__check_source_files_copyright)
    cmake_parse_arguments(
        COPYRIGHT
        ""
        ""
        "INFO;SOURCE_FILES"
        ${ARGN}
    )

    if (NOT COPYRIGHT_INFO)
        return()
    endif()

    # list(GET COPYRIGHT_INFO 1 TEST_INFO)
    # message(${TEST_INFO})
    set(EXT_LIST)
    set(INFO_LIST)
    foreach (INFO ${COPYRIGHT_INFO})
        string(FIND ${INFO} "-" SPLIT_INDEX)
        string(LENGTH ${INFO} INFO_LEN)
        string(SUBSTRING ${INFO} 0 ${SPLIT_INDEX} EXT)
        math(EXPR INFO_INDEX "${SPLIT_INDEX} + 1" DECIMAL)
        string(SUBSTRING ${INFO} ${SPLIT_INDEX} ${INFO_LEN} INFO)
        list(APPEND EXT_LIST ${EXT})
        list(APPEND INFO_LIST ${INFO})
    endforeach()
    message(${EXT_LIST})
    message(${INFO_LIST})

    return()

    set(SOURCE_FILES ${ARGN})
    foreach (SOURCE_FILE_PATH ${COPYRIGHT_SOURCE_FILES})
        get_filename_component(FILE_EXT ${SOURCE_FILE_PATH} EXT)
        list(GET COPYRIGHT_INFO 1 TEST_INFO)
        if (FILE_EXT MATCHES ".(cpp|hpp|inl)$")
            file(
                STRINGS
                ${SOURCE_FILE_PATH}
                COPYRIGHT_INFO
                LIMIT_INPUT ${PROJECT_COPYRIGHT_STR_LEN}
                NO_HEX_CONVERSION
                NEWLINE_CONSUME
            )
            if (
                NOT
                COPYRIGHT_INFO
                STREQUAL
                ${PROJECT_COPYRIGHT}
            )
                message(
                    FATAL_ERROR
                    "\"${SOURCE_FILE_PATH}\" file not copyright info."
                )
            endif()
        endif()
    endforeach()
endfunction()

function(__set_target_property)
    cmake_parse_arguments(
        MODULE
        ""
        "NAME;TYPE;GROUP;CONFIGURATION_TYPE"
        "COPYRIGHT_INFO;ROOT_DIRECTORY;SRC_DIRECTORY;BUILD_DIRECTORY;SOURCE_FILES;INCLUDE_PATHS;RUNTIME_DEPENDENCIES;STATIC_DEPENDENCIES;DEPENDENCY_MODULE_NAMES;PREPROCESSED_FILES;DEFINITIONS;COMPILE_OPTIONS;LINK_OPTIONS"
        ${ARGN}
    )

    # set(MODULE_BINARIES_DIR "${PROJECT_BUILD_DIR}/binaries/${PLATFORM}/${MODULE_PROJECT_NAME}")
    # set(MODULE_LIBRARIES_DIR "${PROJECT_BUILD_DIR}/libraries/${PLATFORM}/${MODULE_PROJECT_NAME}")

    # set(OUTPUT_DIR)
    # if (MODULE_GROUP)
    #     string(REGEX REPLACE "[a-zA-Z0-9_\.-]*/(.*)" "\\1" OUTPUT_DIR ${MODULE_GROUP})
    # endif()

    file(GLOB MODULE_GROUP RELATIVE ${PROJECT_ROOT_DIR} ${MODULE_ROOT_DIR})
    set(BINARIES_DIR "${MODULE_BUILD_DIR}/binaries/${PLATFORM}")
    set(LIBRARIES_DIR "${MODULE_BUILD_DIR}/libraries/${PLATFORM}")
    set(MODULE_BINARIES_DIR "${BINARIES_DIR}/${MODULE_GROUP}")
    set(MODULE_LIBRARIES_DIR "${LIBRARIES_DIR}/${MODULE_GROUP}")

    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY LIBRARY_OUTPUT_DIRECTORY_DEBUG
            ${MODULE_BINARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY LIBRARY_OUTPUT_DIRECTORY_RELEASE
            ${MODULE_BINARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY LIBRARY_OUTPUT_DIRECTORY
            ${MODULE_BINARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY ARCHIVE_OUTPUT_DIRECTORY_DEBUG
            ${MODULE_LIBRARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY ARCHIVE_OUTPUT_DIRECTORY_RELEASE
            ${MODULE_LIBRARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY ARCHIVE_OUTPUT_DIRECTORY
            ${MODULE_LIBRARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY RUNTIME_OUTPUT_DIRECTORY_DEBUG
            ${MODULE_BINARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY RUNTIME_OUTPUT_DIRECTORY_RELEASE
            ${MODULE_BINARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY RUNTIME_OUTPUT_DIRECTORY
            ${MODULE_BINARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY LINKER_LANGUAGE
            CXX
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_TYPE
            ${MODULE_TYPE}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_CONFIGURATION_TYPE
            ${MODULE_CONFIGURATION_TYPE}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_LIBRARIES_DIR
            ${MODULE_LIBRARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_BINARIES_DIR
            ${MODULE_BINARIES_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_ROOT_DIR
            ${MODULE_ROOT_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_SRC_DIR
            ${MODULE_SRC_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_BUILD_DIR
            ${MODULE_BUILD_DIR}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_SOURCE_FILES
            ${MODULE_SOURCE_FILES}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_INCLUDE_PATHS
            ${MODULE_INCLUDE_PATHS}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_RUNTIME_DEPENDENCIES
            ${MODULE_RUNTIME_DEPENDENCIES}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_STATIC_DEPENDENCIES
            ${MODULE_STATIC_DEPENDENCIES}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_DEPENDENCY_MODULE_NAMES
            ${MODULE_DEPENDENCY_MODULE_NAMES}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_PREPROCESSED_FILES
            ${MODULE_PREPROCESSED_FILES}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_DEFINITIONS
            ${MODULE_DEFINITIONS}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_COMPILE_OPTIONS
            ${MODULE_COMPILE_OPTIONS}
    )
    set_property(
        TARGET
            ${MODULE_NAME}
        PROPERTY _MODULE_LINK_OPTIONS
            ${MODULE_LINK_OPTIONS}
    )
endfunction()


function (__add_include_paths MODULE_NAME)
    get_property(MODULE_INCLUDE_PATHS TARGET ${MODULE_NAME} PROPERTY _MODULE_INCLUDE_PATHS)
    foreach(INCLUDE_PATH ${MODULE_INCLUDE_PATHS})
        target_include_directories(${MODULE_NAME} PUBLIC ${INCLUDE_PATH})
    endforeach(INCLUDE_PATH)
endfunction ()

function(__add_definitions MODULE_NAME)
    get_property(MODULE_CONFIGURATION_TYPE TARGET ${MODULE_NAME} PROPERTY _MODULE_CONFIGURATION_TYPE)
    if (${MODULE_CONFIGURATION_TYPE} MATCHES "^static|shared$")
    # if (${MODULE_CONFIGURATION_TYPE} STREQUAL "static" or ${MODULE_CONFIGURATION_TYPE} STREQUAL "shared")
        string(TOUPPER ${MODULE_NAME} MODULE_UPPER_NAME)
        target_compile_definitions(${MODULE_NAME} PUBLIC "-D${MODULE_UPPER_NAME}_LIBRARY")
    endif()
    get_property(MODULE_DEFINITIONS TARGET ${MODULE_NAME} PROPERTY _MODULE_DEFINITIONS)
    foreach (DEFINITION ${MODULE_DEFINITIONS})
        target_compile_definitions(${MODULE_NAME} PUBLIC "-D${DEFINITION}")
    endforeach()
endfunction()

function(__add_preprocessed_files MODULE_NAME)
    get_property(MODULE_STATIC_DEPENDENCIES TARGET ${MODULE_NAME} PROPERTY _MODULE_STATIC_DEPENDENCIES)
    foreach(PREPROCESSED_FILE ${MODULE_PREPROCESSED_FILES})
        if (${PLATFORM} STREQUAL "win32" OR ${PLATFORM} STREQUAL "win64")
            add_definitions("/FI${PREPROCESSED_FILE}")
        elseif (${PLATFORM} STREQUAL "linux" OR ${PLATFORM} STREQUAL "mac")
            add_definitions("-include ${PREPROCESSED_FILE}")
        endif ()
    endforeach()
endfunction ()

function (__add_static_dependencies MODULE_NAME)
    get_property(MODULE_STATIC_DEPENDENCIES TARGET ${MODULE_NAME} PROPERTY _MODULE_STATIC_DEPENDENCIES)
    foreach (STATIC_DEPENDENCY ${MODULE_STATIC_DEPENDENCIES})
        if (EXISTS ${STATIC_DEPENDENCY})
            target_link_libraries(${MODULE_NAME} ${STATIC_DEPENDENCY})
        else ()
            message(FATAL_ERROR "${STATIC_DEPENDENCY} does not exist.")
        endif ()
    endforeach ()
endfunction ()

function (__add_runtime_dependencies MODULE_NAME)
    get_property(MODULE_RUNTIME_DEPENDENCIES TARGET ${MODULE_NAME} PROPERTY _MODULE_RUNTIME_DEPENDENCIES)
    get_property(MODULE_BINARIES_DIR TARGET ${MODULE_NAME} PROPERTY _MODULE_BINARIES_DIR)
    foreach (RUNTIME_DEPENDENCY ${MODULE_RUNTIME_DEPENDENCIES})
        if (NOT EXISTS ${RUNTIME_DEPENDENCY})
            message(FATAL_ERROR "Not fond ${RUNTIME_DEPENDENCY}.")
        endif()
        get_filename_component(FORM_NAME ${RUNTIME_DEPENDENCY} NAME)
        set(SRC_PATH "${RUNTIME_DEPENDENCY}")
        set(DST_PATH "${MODULE_BINARIES_DIR}/${FORM_NAME}")
        __debug_message("Deploying ${SRC_PATH}")
        if (EXISTS ${DST_PATH})
            file(MD5 ${SRC_PATH} SRC_MD5)
            file(MD5 ${DST_PATH} DST_MD5)
            if (${SRC_MD5} STREQUAL ${DST_MD5})
                __debug_message("Already exist ${DST_PATH}")
                continue()
            endif()
        endif()
        file(COPY ${RUNTIME_DEPENDENCY} DESTINATION ${MODULE_BINARIES_DIR})
    endforeach ()
endfunction ()

function(__add_module_dependencies MODULE_NAME)
    get_property(
        MODULE_DEPENDENCY_MODULE_NAMES
        TARGET
            ${MODULE_NAME}
        PROPERTY
            _MODULE_DEPENDENCY_MODULE_NAMES
    )
    foreach (DEPENDENCY_MODULE_NAME ${MODULE_DEPENDENCY_MODULE_NAMES})
        add_dependencies(${MODULE_NAME} ${DEPENDENCY_MODULE_NAME})
        target_link_libraries(${MODULE_NAME} ${DEPENDENCY_MODULE_NAME})
    endforeach()
endfunction ()

function(__add_compile_options MODULE_NAME)
    get_property(
        MODULE_COMPILE_OPTIONS
        TARGET
            ${MODULE_NAME}
        PROPERTY
            _MODULE_COMPILE_OPTIONS
    )
    foreach (COMPILE_OPTION ${MODULE_COMPILE_OPTIONS})
        target_compile_definitions(${MODULE_NAME} PUBLIC ${COMPILE_OPTION})
    endforeach()
endfunction ()

function(__add_link_options MODULE_NAME)
    get_property(
        MODULE_LINK_OPTIONS
        TARGET
            ${MODULE_NAME}
        PROPERTY
            _MODULE_LINK_OPTIONS
    )
    foreach (LINK_OPTION ${MODULE_LINK_OPTIONS})
        target_link_options(${MODULE_NAME} PUBLIC ${LINK_OPTION})
    endforeach()
endfunction ()

function (__generate_env_file MODULE_NAME)
    get_property(
        MODULE_DEPENDENCY_MODULE_NAMES
        TARGET
            ${MODULE_NAME}
        PROPERTY
            _MODULE_DEPENDENCY_MODULE_NAMES
    )
    get_property(
        MODULE_BINARIES_DIR
        TARGET
            ${MODULE_NAME}
        PROPERTY
            _MODULE_BINARIES_DIR
    )

    set(FILE_PATH "${MODULE_BINARIES_DIR}/${MODULE_NAME}.env")
    # file(WRITE ${FILE_PATH} "PATH=%PATH%;")

    set(DATA_BUFFER "PATH=%PATH%")
    foreach (DEPENDENCY_MODULE_NAME ${MODULE_DEPENDENCY_MODULE_NAMES})
        get_property(
            DEPENDENCY_BINARIES_DIR
            TARGET
                ${DEPENDENCY_MODULE_NAME}
            PROPERTY
                _MODULE_BINARIES_DIR
        )
        set(DATA_BUFFER "${DATA_BUFFER};${DEPENDENCY_BINARIES_DIR}")
        # file(APPEND ${FILE_PATH} "${DEPENDENCY_BINARIES_DIR};")
    endforeach()
    if (NOT DATA_BUFFER STREQUAL "PATH=%PATH%")
        file(WRITE ${FILE_PATH} ${DATA_BUFFER})
    endif()
endfunction()

function (add_module)
    cmake_parse_arguments(
        MODULE
        ""
        "NAME;TYPE;GROUP;CONFIGURATION_TYPE"
        "ROOT_DIR;SRC_DIR;BUILD_DIR;SOURCE_FILES;INCLUDE_PATHS;PREPROCESSED_FILES;DEFINITIONS;RUNTIME_DEPENDENCIES;STATIC_DEPENDENCIES;DEPENDENCY_MODULE_NAMES;COMPILE_OPTIONS;LINK_OPTIONS"
        ${ARGN}
    )

    if (${MODULE_CONFIGURATION_TYPE} STREQUAL "executable")
        add_executable(${MODULE_NAME} ${MODULE_SOURCE_FILES})
    elseif (${MODULE_CONFIGURATION_TYPE} STREQUAL "module")
        add_library(${MODULE_NAME} MODULE ${MODULE_SOURCE_FILES})
    elseif (${MODULE_CONFIGURATION_TYPE} STREQUAL "static")
        add_library(${MODULE_NAME} STATIC ${MODULE_SOURCE_FILES})
    elseif (${MODULE_CONFIGURATION_TYPE} STREQUAL "shared")
        add_library(${MODULE_NAME} SHARED ${MODULE_SOURCE_FILES})
    elseif (${MODULE_CONFIGURATION_TYPE} STREQUAL "custom")
        add_custom_target(${MODULE_NAME} SOURCES ${MODULE_SOURCE_FILES})
    else()
        return()
    endif()

    file(GLOB MODULE_GROUP RELATIVE ${PROJECT_ROOT_DIR} ${MODULE_ROOT_DIR})
    __debug_message("Add module - ${MODULE_GROUP}-${MODULE_NAME}.")

    __set_target_property(${ARGV})

    if (NOT ${MODULE_CONFIGURATION_TYPE} STREQUAL "custom")
        __add_definitions(${MODULE_NAME})
        __add_include_paths(${MODULE_NAME})
        __add_module_dependencies(${MODULE_NAME})
        __add_runtime_dependencies(${MODULE_NAME})
        __add_static_dependencies(${MODULE_NAME})
        __add_preprocessed_files(${MODULE_NAME})
        __add_compile_options(${MODULE_NAME})
        __add_link_options(${MODULE_NAME})
    endif()

    # if (${MODULE_CONFIGURATION_TYPE} STREQUAL "executable")
    #     __generate_env_file(${MODULE_NAME})
    # endif()

    if (MSVC)
        # file(GLOB MODULE_GROUP RELATIVE ${PROJECT_SRC_DIR} ${MODULE_DIRECTORY})
        # string(REGEX MATCH "([a-zA-Z0-9_\.-]*/[0-9a-zA-Z_\.-]*)" MODULE_GROUP ${MODULE_GROUP})
        foreach(SOURCE_FILE_PATH ${MODULE_SOURCE_FILES})
            get_filename_component(FILE_PATH ${SOURCE_FILE_PATH} PATH)
            file(GLOB FILE_PATH RELATIVE ${MODULE_SRC_DIR} ${FILE_PATH})
            if (NOT FILE_PATH)
                source_group("" FILES ${SOURCE_FILE_PATH})
                continue()
            endif()
            if (${FILE_PATH} MATCHES "\\.\\.")
                source_group("" FILES ${SOURCE_FILE_PATH})
                continue()
            endif()
            string(REPLACE "/" "\\\\\\\\" FILE_PATH ${FILE_PATH})
            source_group(${FILE_PATH} FILES ${SOURCE_FILE_PATH})
        endforeach()
        set_target_properties(${MODULE_NAME} PROPERTIES FOLDER "${MODULE_GROUP}")
    endif()
endfunction()
