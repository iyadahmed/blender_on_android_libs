import os
from pathlib import Path
import tarfile

import requests
from tqdm import tqdm

BLENDER_SVN_PKGS_ROOT = "https://svn.blender.org/svnroot/bf-blender/trunk/lib/packages/"

SOURCES_DOWNLOAD_PATH = Path(".") / "sources"
if not SOURCES_DOWNLOAD_PATH.exists():
    os.mkdir(SOURCES_DOWNLOAD_PATH)


def download_pkg_source(pkg_filename: str) -> Path:
    url = f"{BLENDER_SVN_PKGS_ROOT}/{pkg_filename}"
    save_path = SOURCES_DOWNLOAD_PATH / pkg_filename

    with requests.get(url, stream=True) as download_stream, open(
        save_path, "wb"
    ) as file:
        download_stream.raise_for_status()

        # Progress bar for file downloads: https://stackoverflow.com/a/42071418/8094047
        # + unit_scale=True and unit_divisor=1000
        file_size = int(download_stream.headers["Content-Length"])
        pbar = tqdm(unit="B", total=file_size, unit_scale=True, unit_divisor=1000)

        for chunk in download_stream.iter_content(chunk_size=1024 * 1024):
            file.write(chunk)
            pbar.update(len(chunk))

    return save_path


download_pkg_source("brotli-v1.0.9.tar.gz")
download_pkg_source("libepoxy-1.5.10.tar.gz")
download_pkg_source("freetype-2.12.1.tar.gz")
download_pkg_source("libjpeg-turbo-2.1.3.tar.gz")
download_pkg_source("libpng-1.6.37.tar.xz")
download_pkg_source("Python-3.10.9.tar.xz")
download_pkg_source("zstd-1.5.0.tar.gz")
