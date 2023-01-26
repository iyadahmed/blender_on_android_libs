#!/bin/sh
set -e

#TODO: remove hardcoded paths

tar xzf libjpeg-turbo-2.1.3.tar.gz
cd libjpeg-turbo-2.1.3
mkdir build
cd build
cmake .. \
-DCMAKE_INSTALL_PREFIX=/home/iyad/Development/Blender_On_Android/lib/android_aarch64/jpeg \
-DCMAKE_SYSTEM_NAME=Android \
-DCMAKE_SYSTEM_VERSION=21 \
-DCMAKE_ANDROID_ARCH_ABI=arm64-v8a \
-DCMAKE_ANDROID_NDK=/home/iyad/Android/Sdk/ndk/25.1.8937393 \
-DCMAKE_ANDROID_STL_TYPE=c++_static
make install
