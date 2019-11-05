import argparse

import slice


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="relative path to the video file")
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        help="relative path to output directory",
                        required=False,
                        default="output/")
    args = parser.parse_args()

    videoPrism = slice.loadVideo(args.path)
    slice.randomProjectionSlice(videoPrism, args.path, 100, args.output)


if __name__ == "__main__":
    main()
