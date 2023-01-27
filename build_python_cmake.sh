#!/bin/sh
set -e

#TODO: remove hardcoded paths
#NOTE: you need a running virtual android device with arm64-v8a and android 5.0 at least!
# so that CMake can run some pre-compile check binaries on the target system when cross compiling

#git clone https://github.com/python-cmake-buildsystem/python-cmake-buildsystem.git
#git clone https://github.com/jcfr/python-cmake-buildsystem.git
cd python-cmake-buildsystem-jcfr

mkdir build
cd build
cmake .. \
-DCMAKE_INSTALL_PREFIX=/home/iyad/Development/Blender_On_Android/lib/android_aarch64/python \
-DCMAKE_SYSTEM_NAME=Android \
-DCMAKE_SYSTEM_VERSION=21 \
-DCMAKE_ANDROID_ARCH_ABI=arm64-v8a \
-DCMAKE_ANDROID_NDK=/home/iyad/Android/Sdk/ndk/25.1.8937393 \
-DCMAKE_ANDROID_STL_TYPE=c++_static \
-DCMAKE_CROSSCOMPILING_EMULATOR=../run_on_android.sh \
-DANDROID_ALLOW_UNDEFINED_SYMBOLS=ON \
-DENABLE_DECIMAL=OFF \
-DENABLE_CTYPES=OFF

make install
