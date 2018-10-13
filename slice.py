# Outputs the image produced by slicing through the prism with an arbitary plane

import imageio
import numpy as np
from PIL import Image
from tqdm import tqdm

def main():
    XC = -0.1
    YC = 0.1
    C  = 0.6
    FILENAME = "cat.mp4"
    #TODO: arg this
    path = "videos/" + FILENAME
    videoPrism = loadVideo(path)

    randomProjectionSlice(videoPrism,FILENAME,20)

def loadVideo(videoPath):
    firstFrame = True
    reader = imageio.get_reader(videoPath)
    nFrames = reader.get_meta_data()['nframes'];
    framesArr = []
    for _ in tqdm(range(nFrames)):
        try:
            frame = reader.get_next_data()
        #This occurs at the end of the file
        except imageio.core.CannotReadFrameError:
            break
        else:
            framesArr.append(np.asarray(frame))
            
    #print(framesArr)
    prism = np.stack(framesArr,axis = 0)
    return prism

def projectionSlice(videoPrism, xc,yc,c):
    c = int(map(c,0.0,1.0,0,videoPrism.shape[0]))
    #print(videoPrism.shape)
    #print(c)
    projection = np.zeros(shape = (videoPrism.shape[2],videoPrism.shape[1],3))
    for x in tqdm(range(videoPrism.shape[2])):
        for y in tqdm(range(videoPrism.shape[1])):
            z = int ((xc * x) + (yc * y) + c)
            #print(z)
            try:
                projection[x,y] = videoPrism[z,y,x]
            except:
                #print("out of bounds")
                continue
    
    #projection = projection.astype(np.uint8)
    #print(projection.shape)
    #print(projection[100,10])
    img = Image.fromarray(projection.astype(np.uint8),'RGB')
    return img

def saveImage(img,xc,yc,c,fileName):
    img.save("output/" + str(fileName) +  str(xc) + str(yc) + str(c) + ".png" )

def randomProjectionSlice(videoPrism,fileName, num):
    for _ in tqdm(range(num)):
        xc = np.random.uniform(-1.5,1.5)
        yc = np.random.uniform(-1.5,1.5)
        c  = np.random.uniform(0.25,0.75)
        img = projectionSlice(videoPrism, xc, yc, c)
        saveImage(img,xc,yc,c,fileName)
        

def map( x,  in_min,  in_max,  out_min,  out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

if __name__ == "__main__":
    main()
