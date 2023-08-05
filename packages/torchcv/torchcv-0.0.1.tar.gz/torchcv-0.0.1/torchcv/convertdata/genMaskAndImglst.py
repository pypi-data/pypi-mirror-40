from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
from PIL import Image
from PIL import ImageDraw 
import os


def getCocoLst(dataDir, dataType, imagePath, labelPath, instanceSize):
    '''
    import argparse


    parser = argparse.ArgumentParser(description='get instance images datasets ')

    parser.add_argument('--dataDir', type=str, default='/Volumes/DATASET/COCODatasets/COCO2017',
                        help='directory of datasets')
    parser.add_argument('--dataType', type=str, default='val2017',
                        help='datasets name')
    parser.add_argument('--labelPath', type=str, default='/Volumes/DATASET/COCODatasets/COCO2017segDataset/lable',
                        help='directory of saved instance mask')
    parser.add_argument('--imagePath', type=str, default='/Volumes/DATASET/COCODatasets/COCO2017segDataset/image',
                        help='directory of saved instance images')
    parser.add_argument('--instanceSize', type=float, default=0.0,
                        help='directory of saved instance images')

    opt = parser.parse_args()
    '''
    annFile='{}/annotations/instances_{}.json'.format(dataDir, dataType)
    dataDir = dataDir
    dataType = dataType
    image_path = imagePath
    label_path= labelPath
    instance_size = instanceSize

    # python genMaskAndImg.py --dataType val2017 --dataDir /data1/datasets/coco --labelPath /data1/datasets/coco/seg_val2017/label --imagePath /data1/datasets/coco/seg_val2017/image
    # python genMaskAndImg.py --dataType train2017 --dataDir /data1/datasets/coco --labelPath /data1/datasets/coco/seg_train2017/label --imagePath /data1/datasets/coco/seg_train2017/image  --instanceSize 900



    # initialize COCO api for instance annotations
    coco=COCO(annFile)
    cats = coco.loadCats(coco.getCatIds())
    nms=[cat['name'] for cat in cats] 


    with open('.coco_instance.lst','rw') as f:
        i = 0
        for nm in nms:
            # get all images containing given categories, select one at random
            catIds = coco.getCatIds(catNms=[nm]);
            # print(catIds)[1, 3, 18, 41]
            # all image ids
            imgIds = coco.getImgIds(catIds=catIds);
            # print(len(imgIds))
            # all images
            imgs = coco.loadImgs(imgIds)
            print('categorie:', nm)
            for img in imgs:
                # get image annIds
                annIds = coco.getAnnIds(imgIds=[img['id']], catIds=catIds, iscrowd=0)
                # print('image', img['id'], annIds)
                anns = coco.loadAnns(annIds)
                # print(anns)
                for ann in anns:  
                    if ann['iscrowd'] == 0 and ann['area'] >= instance_size:
                        # label_path image_path
                        # saveImg(image_path, crop_img, nm,)
            
                        image_path = os.path.join('image', nm , str(img['id']) + '_' + str(ann['id']) + '.JPEG')
                        label_path = os.path.join('label', nm , str(img['id']) + '_' + str(ann['id']) + '.JPEG')
                        f.write(str(i) +','+ label_path+ ',' + image_path + ',' +ann['area'] +'\n')
