import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
from PIL import Image
from PIL import ImageDraw 
import os
import json

def imageGenMask(imageMask, polygon, bbox):
  
    imgDraw = ImageDraw.Draw(imageMask) 

    # for polygon in ann['segmentation']:
    imgDraw.polygon(tuple(polygon), fill = 1)  
    # draw.polygon(box, 'olive', 'hotpink')
    # imagelabel.show()#hotpink
    # bbox = ann['bbox']
#     print('id',ann['id'])
    imagecrop = imageMask.crop(bbox)
    imagecrop = np.array(imagecrop) * 255
    plt.imshow(imagecrop)
    plt.show()
    return Image.fromarray(imagecrop)




data = json.load(open('/Volumes/DATASET/Cityscapes_office/gtFine_trainvaltest/gtFine/val/lindau/lindau_000000_000019_gtFine_polygons.json','r'))

array = np.ndarray((data['imgHeight'], data['imgWidth'], 3), np.uint8)  
array[:, :, 0] = 0  
array[:, :, 1] = 0  
array[:, :, 2] = 0  


for obj in data['objects']:
    # print(obj['label'])
    if obj['label']== 'car':
        segs = np.array(obj['polygon'])
        x1 = min(segs[:,0])  
        x2 = max(segs[:,0]) 
        y1 = min(segs[:,1])  
        y2 = max(segs[:,1]) 
        area = (y2-y1)*(x2-x1)
        print(area)
        imageMask = Image.fromarray(array)
        imageGenMask(imageMask, segs.reshape(-1,1),[x1,y1,x2,y2])
