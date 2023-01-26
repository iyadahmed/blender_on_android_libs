#!/bin/sh
set -e

#TODO: remove hardcoded paths

tar xzf libepoxy-1.5.10.tar.gz
cd libepoxy-1.5.10
mkdir build
cd build

meson \
-Dprefix=/home/iyad/Development/Blender_On_Android/lib/android_aarch64/epoxy \
--cross-file ../../meson_cross/android-aarch64.ini \
-Dx11=false

ninja
ninja install

