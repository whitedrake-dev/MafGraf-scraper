#!/usr/bin/env python3
import sys
from PIL import Image

def images_differ(path1, path2):
    """
    Return True if images differ, False if they are identical.
    """

    try:
        img1 = Image.open(path1)
        img2 = Image.open(path2)
    except Exception as e:
        raise RuntimeError(f"Failed to open images: {e}")

    # Compare size first (fast)
    if img1.size != img2.size:
        return True

    # Compare mode (RGB, RGBA, etc.)
    if img1.mode != img2.mode:
        return True

    # Compare pixel data
    # This loads raw bytes and compares them directly
    data1 = img1.tobytes()
    data2 = img2.tobytes()

    return data1 != data2


def main():
    if len(sys.argv) != 3:
        print("Usage: compare_images.py <image1> <image2>")
        sys.exit(2)

    path1, path2 = sys.argv[1], sys.argv[2]

    try:
        differ = images_differ(path1, path2)
    except Exception as e:
        print("Error:", e)
        sys.exit(2)

    if differ:
        print("Images differ.")
        sys.exit(1)
    else:
        print("Images are identical.")
        sys.exit(0)


if __name__ == "__main__":
    main()
