#!/bin/sh
set -e

#TODO: remove hardcoded paths

tar xzf freetype-2.12.1.tar.gz
cd freetype-2.12.1
mkdir build
cd build

# build brotli first!

cmake .. \
-DCMAKE_INSTALL_PREFIX=/home/iyad/Development/Blender_On_Android/lib/android_aarch64/freetype \
-DCMAKE_SYSTEM_NAME=Android \
-DCMAKE_SYSTEM_VERSION=21 \
-DCMAKE_ANDROID_ARCH_ABI=arm64-v8a \
-DCMAKE_ANDROID_NDK=/home/iyad/Android/Sdk/ndk/25.1.8937393 \
-DCMAKE_ANDROID_STL_TYPE=c++_static \
-DCMAKE_FIND_ROOT_PATH=/home/iyad/Development/Blender_On_Android/lib/android_aarch64/brotli/ \
-DFT_REQUIRE_BROTLI=ON

make install
