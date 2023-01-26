#!/bin/sh
set -e

#TODO: remove hardcoded paths

tar xf libpng-1.6.37.tar.xz
cd libpng-1.6.37
mkdir build
cd build
cmake .. \
-DCMAKE_INSTALL_PREFIX=/home/iyad/Development/Blender_On_Android/lib/android_aarch64/png \
-DCMAKE_SYSTEM_NAME=Android \
-DCMAKE_SYSTEM_VERSION=21 \
-DCMAKE_ANDROID_ARCH_ABI=arm64-v8a \
-DCMAKE_ANDROID_NDK=/home/iyad/Android/Sdk/ndk/25.1.8937393 \
-DCMAKE_ANDROID_STL_TYPE=c++_static \
-DHAVE_LD_VERSION_SCRIPT=OFF
# Previous option needed for libpng to compile for Android
#https://stackoverflow.com/a/62541328/8094047

make install
