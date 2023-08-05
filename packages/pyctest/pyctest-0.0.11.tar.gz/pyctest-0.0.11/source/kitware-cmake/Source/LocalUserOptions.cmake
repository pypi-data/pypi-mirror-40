################################################################################
#
#       CMAKE
#
################################################################################

set(_CMAKE_LIBRARIES
    CMakeLib
    cmsys
    ${CMAKE_EXPAT_LIBRARIES}
    ${CMAKE_ZLIB_LIBRARIES}
    ${CMAKE_TAR_LIBRARIES}
    ${CMAKE_COMPRESS_LIBRARIES}
    ${CMAKE_CURL_LIBRARIES}
    ${CMAKE_JSONCPP_LIBRARIES}
    ${CMAKE_LIBUV_LIBRARIES}
    ${CMAKE_LIBRHASH_LIBRARIES}
    ${CMake_KWIML_LIBRARIES}
)
set(_CMAKE_LIBRARY_UTILITIES
    BZIP2 CURL EXPAT FORM JSONCPP LIBARCHIVE LIBLZMA LIBRHASH LIBUV ZLIB)

foreach(_PACKAGE ${_CMAKE_LIBRARY_UTILITIES})
    if(NOT CMAKE_USE_SYSTEM_${_PACKAGE} AND ${_PACKAGE}_LIBRARY)
        list(APPEND _CMAKE_LIBRARIES ${${_PACKAGE}_LIBRARY})
    endif()
endforeach()

list(REMOVE_DUPLICATES _CMAKE_LIBRARIES)

export(TARGETS ${_CMAKE_LIBRARIES}
    FILE ${CMAKE_BINARY_DIR}/CMakeLibBuild.cmake)

set_property(GLOBAL PROPERTY CMAKE_PROJECT_LIBRARIES ${_CMAKE_LIBRARIES})

################################################################################
#
#       CTEST
#
################################################################################

set(_CTEST_LIBRARIES
    CTestLib
    ${CMAKE_CURL_LIBRARIES}
    ${CMAKE_XMLRPC_LIBRARIES}
)

# check if built or using system
set(_CTEST_LIBRARY_UTILITIES
    BZIP2 CURL EXPAT FORM JSONCPP LIBARCHIVE LIBLZMA LIBRHASH LIBUV ZLIB)

# assemble list
foreach(_PACKAGE ${_CTEST_LIBRARY_UTILITIES})
    if(NOT CMAKE_USE_SYSTEM_${_PACKAGE} AND ${_PACKAGE}_LIBRARY)
        list(APPEND _CTEST_LIBRARIES ${${_PACKAGE}_LIBRARY})
    endif()
endforeach()

list(REMOVE_DUPLICATES _CTEST_LIBRARIES)

export(TARGETS ${_CTEST_LIBRARIES}
    FILE ${CMAKE_BINARY_DIR}/CTestLibBuild.cmake)

set_property(GLOBAL PROPERTY CTEST_PROJECT_LIBRARIES ${_CTEST_LIBRARIES})

################################################################################
#
#       CPACK
#
################################################################################

set(_CPACK_LIBRARIES
    CPackLib
    ${CMAKE_CURL_LIBRARIES}
    ${CMAKE_XMLRPC_LIBRARIES}
)

# check if built or using system
set(_CPACK_LIBRARY_UTILITIES
    BZIP2 CURL EXPAT FORM JSONCPP LIBARCHIVE LIBLZMA LIBRHASH LIBUV ZLIB)

# assemble list
foreach(_PACKAGE ${_CPACK_LIBRARY_UTILITIES})
    if(NOT CMAKE_USE_SYSTEM_${_PACKAGE} AND ${_PACKAGE}_LIBRARY)
        list(APPEND _CPACK_LIBRARIES ${${_PACKAGE}_LIBRARY})
    endif()
endforeach()

list(REMOVE_DUPLICATES _CPACK_LIBRARIES)

export(TARGETS ${_CPACK_LIBRARIES}
    FILE ${CMAKE_BINARY_DIR}/CPackLibBuild.cmake)

set_property(GLOBAL PROPERTY CPACK_PROJECT_LIBRARIES ${_CPACK_LIBRARIES})

################################################################################
#
#       INSTALLATION
#
################################################################################
set(_INSTALL_LIBRARIES ${_CMAKE_LIBRARIES} ${_CTEST_LIBRARIES} ${_CPACK_LIBRARIES})
list(REMOVE_DUPLICATES _INSTALL_LIBRARIES)

configure_file(${PROJECT_SOURCE_DIR}/Templates/CMakeDevelConfig.cmake.in
    ${PROJECT_BINARY_DIR}/CMakeDevelConfig.cmake @ONLY)

option(CMake_INSTALL_Devel "Install libraries for development" OFF)
if(CMake_INSTALL_Devel)
    include(GNUInstallDirs)

    install(TARGETS ${_INSTALL_LIBRARIES}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}
        EXPORT CMakeDevelDepends)

    install(EXPORT CMakeDevelDepends
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)

    install(FILES ${PROJECT_BINARY_DIR}/CMakeDevelConfig.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)
endif()

################################################################################
