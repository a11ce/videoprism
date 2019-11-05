# videoPrism

> What follows from the idea that videos are 3D arrays of pixels? 

## Setup

- Get prerequisites with `pip3 install tqdm numpy imageio pillow`
- Download with `https://github.com/a11ce/transliterator.git`
- Put some source videos in `videos/`

## Usage

- The easiest way to use videoPrism is with `randomSlice.py`. Just run `python3 randomSlice.py videos/<yourFile>` and 100 random slices will be saved in `output/<yourFile>/`. You can also supply a different output path with `-o path/`.
- To generate (frames of) a video of a vertically moving slice with constant slope, run `python3 movingSlice.py videos/<yourfile> <xc> <yc>` where xc and yc are the x and y slope coefficients.
- For more advanced usage, `import slice`. See `movingSlice.py` for an example of custom usage.

---

All contributions are welcome by pull request or issue.

videoPrism is licensed under GNU General Public License v3.0. See [LICENSE](../master/LICENSE) for full text.