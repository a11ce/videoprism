import argparse
from tqdm import tqdm
import numpy as np
import slice


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="relative path to the video file")
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        help="relative path to output directory",
                        required=False,
                        default="")
    parser.add_argument("xc", help="x-coefficient", type=float)
    parser.add_argument("yc", help="y-coefficient", type=float)
    args = parser.parse_args()

    videoPrism = slice.loadVideo(args.path)

    for c in tqdm(np.linspace(0, 1, videoPrism.shape[0]),
                  desc="Slice Movement"):
        img = slice.projectionSlice(videoPrism, args.xc, args.yc, c)
        slice.saveImage(img, args.xc, args.yc, c, args.path, args.output)


if __name__ == "__main__":
    main()
