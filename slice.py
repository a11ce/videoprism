import imageio
import numpy as np
from PIL import Image
from tqdm import tqdm
import os


def main():
    XC = -0.1
    YC = 0.1
    C = 0.6
    FILENAME = "cat.mp4"
    #TODO: arg this
    path = "videos/" + FILENAME
    videoPrism = loadVideo(path)
    randomProjectionSlice(videoPrism, path, 100, "output/")


def loadVideo(videoPath):
    """
    Loads a video located at videoPath and returns it as a numpy array with
    shape (nFrames, height, width, 3). The 3 is for RGB and each pixel is
    treated atomically, so the prism is effectively a 3D array of pixels.
    """
    reader = imageio.get_reader(videoPath)
    framesArr = [np.asarray(frame) for idx, frame in enumerate(reader)]
    prism = np.stack(framesArr, axis=0)
    return prism


def projectionSlice(videoPrism, xc, yc, c):
    """
    Gets a top-down-view specified slice of a videoPrism. xc and yc are the 
    x and y slope coefficients, and c is the (constant) starting height. 
    c is in the range [0,1.0], scaled to the height (aka number of frames).
    """

    # scale c to the video height
    c = int(c * videoPrism.shape[0])

    # begin with a 2D array of black pixels the size of one frame
    projection = np.zeros(shape=(videoPrism.shape[2], videoPrism.shape[1], 3))

    # loop through x and y in the frame
    for x in tqdm(range(videoPrism.shape[2]), desc="Slicing video (x)"):
        for y in range(videoPrism.shape[1]):
            # calculate z (height) according to the slopes and offset
            z = int((xc * x) + (yc * y) + c)
            try:
                # copy the pixel at the correct location to the output image
                projection[x, y] = videoPrism[z, y, x]
            except IndexError:
                # if the point would be above or below the prism,
                # just leave it black
                continue

    # create an image from the array of pixels and do some transformations
    # so the image is correctly displayed
    img = Image.fromarray(projection.astype(np.uint8), 'RGB')
    img = img.transpose(Image.ROTATE_270)
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def saveImage(img, xc, yc, c, fileName, outputDir):
    """
    Write the img to:
    outputDir/videoName/videoName_xc_yx_c.png
    For example:
    output/cat.mp4/cat.mp4_-1_1_0.5.png

    A videoName folder inside outputDir is used so that multiple runs on the
    same source video are easily grouped together. Slice information is saved
    within the filename so that the user can explore slices near any 
    interesting random/previous ones.
    """
    endOfName = fileName.split("/")[-1]
    folder = (outputDir + endOfName + "/")
    os.makedirs(folder, exist_ok=True)
    img.save(folder + str(endOfName) + "_" + str(xc) + "_" + str(yc) + "_" +
             str(c) + ".png")


def randomProjectionSlice(videoPrism, fileName, num, outputDir):
    """
    Generates and saves num random slices using the given prism.
    fileName and outputDir are passed on to saveImage.
    """

    nFrames = videoPrism.shape[0]
    sideLength = (videoPrism.shape[1] + videoPrism.shape[2]) / 2

    # the upper and lower bounds for xc and yc are derived from the number of
    # frames and the average side length
    upBound = (nFrames / (sideLength * 4))
    lowBound = -1 * upBound
    print("bound is " + str(upBound))

    for _ in tqdm(range(num), desc="Random projections"):
        xc = np.random.uniform(lowBound, upBound)
        yc = np.random.uniform(lowBound, upBound)

        # c is between 25% and 75% of the upper bound
        c = np.random.uniform((upBound / 4), (1 - (upBound / 4)))
        img = projectionSlice(videoPrism, xc, yc, c)
        saveImage(img, xc, yc, c, fileName, outputDir)


if __name__ == "__main__":
    main()
