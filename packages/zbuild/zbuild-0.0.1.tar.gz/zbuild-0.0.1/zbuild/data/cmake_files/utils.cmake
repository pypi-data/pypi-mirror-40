
function(__debug_message)
    string(REPLACE ";" " " __msg "${ARGN}")
    message(STATUS "${__msg}")
endfunction()

function(__remove_duplicates __list)
    if(${__list})
        list(REMOVE_DUPLICATES ${__list})
    endif()
endfunction()