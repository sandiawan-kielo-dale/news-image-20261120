"""Copy the front-page image to the output directory.

Stdlib only: os, shutil, struct, sys.
"""
import os
import shutil
import struct
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./out")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        sys.stderr.write("entry.png is not a PNG\n")
        return 1
    width, height = struct.unpack(">II", head[16:24])
    print("wrote %s (%dx%d)" % (dst, width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
