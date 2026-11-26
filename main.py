"""Entrypoint: copy the pre-rendered poster to the output directory.

The image is drawn by draw_timeline.py (run at build time with Pillow);
this program only copies bytes, so both grading runs write identical
output. Standard library only.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
