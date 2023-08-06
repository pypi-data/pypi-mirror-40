#ifndef ROOT_RConfigOptions
#define ROOT_RConfigOptions

#define R__CONFIGUREOPTIONS   "Backtrace_INCLUDE_DIR=/usr/include DL_LIBRARY_PATH=/usr/lib/libdl.dylib LIBCLANG_LIBRARY_VERSION=5.0 LIBXML2_INCLUDE_DIR=/opt/local/include/libxml2 LIBXML2_LIBRARY=/opt/local/lib/libxml2.dylib LLVM_INCLUDE_EXAMPLES=OFF LLVM_INCLUDE_RUNTIMES=ON LLVM_INCLUDE_TOOLS=ON LLVM_INCLUDE_UTILS=ON PC_LIBXML_INCLUDEDIR=/opt/local/include PC_LIBXML_INCLUDE_DIRS=/opt/local/include/libxml2 PC_LIBXML_LIBRARIES=xml2 PC_LIBXML_LIBRARY_DIRS=/opt/local/lib PC_LIBXML_STATIC_INCLUDE_DIRS=/opt/local/include/libxml2 PC_LIBXML_STATIC_LIBRARY_DIRS=/opt/local/lib ZLIB_INCLUDE_DIR=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/zlib ZLIB_INCLUDE_DIRS=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/zlib ZLIB_LIBRARIES=ZLIB::ZLIB ZLIB_LIBRARY=$<TARGET_FILE:ZLIB> xxHash_INCLUDE_DIR=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/xxhash xxHash_INCLUDE_DIRS=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/xxhash xxHash_LIBRARIES=xxHash::xxHash xxHash_LIBRARY=$<TARGET_FILE:xxhash> "
#define R__CONFIGUREFEATURES  " builtin_llvm builtin_clang builtin_pcre builtin_xxhash builtin_zlib cling cxx17 explicitlink libcxx thread"

#endif
