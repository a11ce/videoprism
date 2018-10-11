# Outputs the image produced by slicing through the prism with an arbitary plane

import imageio
import numpy as np
from PIL import Image

def main():
    #TODO: arg this
    path = "okgoscaled.mov"
    videoPrism = loadVideo(path)
    projectionSlice(videoPrism,2,1,0.2)

def loadVideo(videoPath):
    firstFrame = True
    reader = imageio.get_reader(videoPath)
    framesArr = []
    while True:
        try:
            frame = reader.get_next_data()
        #This occurs at the end of the file
        except imageio.core.CannotReadFrameError:
            break
        else:
            frameNP = np.asarray(frame)
            framesArr.append(frameNP)
            
    #print(framesArr)
    prism = np.stack(framesArr,axis = 0)
    return prism

def projectionSlice(videoPrism, xc,yc,c):
    c = int(map(c,0.0,1.0,0,videoPrism.shape[0]))
    print(videoPrism.shape)
    print(c)
    projection = np.zeros(shape = (videoPrism.shape[2],videoPrism.shape[1],3))
    for x in range(videoPrism.shape[2]):
        for y in range(videoPrism.shape[1]):
            z = (xc * x) + (yc * y) + c
            try:
                projection[x,y] = videoPrism[z,y,x]
            except:
                #print("out of bounds")
                continue
    
    projection = projection.astype(np.uint8)
    print(projection.shape)
    print(projection[100,10])
    img = Image.fromarray(projection,'RGB')
    img.show()
    
def map( x,  in_min,  in_max,  out_min,  out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

if __name__ == "__main__":
    main()
