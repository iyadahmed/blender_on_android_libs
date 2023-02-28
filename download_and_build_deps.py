import multiprocessing as mp
import os
import platform
import shutil
import subprocess as sp
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import requests
from tqdm import tqdm

BLENDER_SVN_PKGS_ROOT = "https://svn.blender.org/svnroot/bf-blender/trunk/lib/packages/"

SOURCES_DOWNLOAD_PATH = Path(".") / "sources"
if not SOURCES_DOWNLOAD_PATH.exists():
    os.mkdir(SOURCES_DOWNLOAD_PATH)

LIB_BUILD_OUTPUT_PATH = (Path(".") / "build/lib/android_aarch64").absolute()
if not LIB_BUILD_OUTPUT_PATH.exists():
    os.makedirs(LIB_BUILD_OUTPUT_PATH)


def find_android_ndk():
    home = Path.home()
    system_name = platform.system()

    if system_name == "Linux":
        return home / "Android/Sdk/ndk/25.1.8937393"

    elif system_name == "Windows":
        return home / "AppData/Local/Android/Sdk/ndk/25.1.8937393"

    elif system_name == "Darwin":
        return home / "Library/Android/sdk/ndk/25.1.8937393"

    else:
        raise NotImplementedError


NDK = os.getenv("ANDROID_NDK", find_android_ndk())
API = 21
ABI = "arm64-v8a"


def download_file(url: str, save_path: Path) -> Path:
    with requests.get(url, stream=True) as download_stream, open(save_path, "wb") as file:
        download_stream.raise_for_status()

        # Progress bar for file downloads: https://stackoverflow.com/a/42071418/8094047
        # + unit_scale=True and unit_divisor=1000
        file_size = int(download_stream.headers["Content-Length"])
        pbar = tqdm(unit="B", total=file_size, unit_scale=True, unit_divisor=1000)

        for chunk in download_stream.iter_content(chunk_size=1024 * 1024):
            file.write(chunk)
            pbar.update(len(chunk))

    return save_path


def download_pkg_source(pkg_filename: str):
    save_path = SOURCES_DOWNLOAD_PATH / pkg_filename

    if save_path.exists():
        print(f"Skipping download, {pkg_filename} already downloaded.")
        return save_path

    url = f"{BLENDER_SVN_PKGS_ROOT}/{pkg_filename}"
    return download_file(url, save_path)


def build_pkg_cmake(
    pkg_name: str, pkg_filename: str, extra_cmake_build_args: Optional[List[str]] = None, source_dir: str = "."
):
    filepath = download_pkg_source(pkg_filename)
    with tarfile.open(filepath) as file:
        top_dir = os.path.commonpath(file.getnames())
        assert top_dir != "."
        file.extractall(SOURCES_DOWNLOAD_PATH)

    if extra_cmake_build_args is None:
        extra_cmake_build_args = []

    sp.run(
        [
            "cmake",
            "-S",
            source_dir,
            "-B",
            "_build",
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DCMAKE_INSTALL_PREFIX={LIB_BUILD_OUTPUT_PATH / pkg_name}",
            "-DCMAKE_SYSTEM_NAME=Android",
            f"-DCMAKE_SYSTEM_VERSION={API}",
            f"-DCMAKE_ANDROID_ARCH_ABI={ABI}",
            f"-DCMAKE_ANDROID_NDK={NDK}",
            "-DCMAKE_ANDROID_STL_TYPE=c++_static",
            *extra_cmake_build_args,
        ],
        cwd=SOURCES_DOWNLOAD_PATH / top_dir,
    )
    sp.run(
        ["cmake", "--build", ".", "--config", "Release", "-j", f"{mp.cpu_count()}"],
        cwd=SOURCES_DOWNLOAD_PATH / top_dir / "_build",
    )
    sp.run(["cmake", "--install", "."], cwd=SOURCES_DOWNLOAD_PATH / top_dir / "_build")


if __name__ == "__main__":
    build_pkg_cmake("brotli", "brotli-v1.0.9.tar.gz")
    build_pkg_cmake(
        "freetype",
        "freetype-2.12.1.tar.gz",
        [f"-DCMAKE_FIND_ROOT_PATH={LIB_BUILD_OUTPUT_PATH / 'brotli'}", f"-DFT_REQUIRE_BROTLI=ON"]
        # Brotli needs to be built before this
    )
    build_pkg_cmake("jpeg", "libjpeg-turbo-2.1.3.tar.gz")
    build_pkg_cmake(
        "png",
        "libpng-1.6.37.tar.xz",
        ["-DHAVE_LD_VERSION_SCRIPT=OFF"]
        # Cross-compiling for Android fails without the previous option
        # https://stackoverflow.com/a/62541328/8094047
    )
    build_pkg_cmake("zstd", "zstd-1.5.0.tar.gz", source_dir="build/cmake")

    # TODO: build_pkg_meson function
    download_pkg_source("libepoxy-1.5.10.tar.gz")

    # TODO:
    # clone python-cmake-buildsystem and build it
    download_pkg_source("Python-3.10.9.tar.xz")
