        
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# pylint: disable=unused-import

import numpy as np
from PIL import Image, ImageFilter


class BgGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


class BlurryBg(object):

    '''
    """Convert a image to  a image with blurry background.

    Parameters
    ----------
    radius: int
        see ImageFilter.Filter
    bounds: int
        ImageFilter.Filter
    to_tensor: boolean
        default False. if true,the output image will be torch.tensor and the shape will be changed.
        output image  [channels x height x width] eg:  torch.Size([3, 426, 640])
    out: numpy.array
        default output image shape :[height x width x channels] eg: (426, 640, 3)

    example:
        in_img = '/Users/AaronLeong/deeplearning/test_img/demo.jpg'
        mask_img = '/Users/AaronLeong/deeplearning/test_img/demo_blur.jpg'
        blurry_image = blur_bg(10)(in_img,mask_img)

        blurry_image.shape => (426, 640, 3)
    '''
    name = "GaussianBlurBackground"
    
    def __init__(self, radius=2, bounds=None, to_tensor=False):
        self.to_tensor = to_tensor
        if to_tensor:
            from torchvision import transforms
            self.toTensor = transforms.ToTensor()
        self.bgGaussianBlur = BgGaussianBlur(radius=radius,bounds=bounds)
    
    def __call__(self, img_path, mask_path):
        image = Image.open(img_path)
        ori_image = np.array(image)
        blur_image = np.array(image.filter(self.bgGaussianBlur))
        mask = np.array(Image.open(mask_path))

        mask = np.array(mask)>0     
        res_image = ori_image*mask + blur_image*(1-mask)
        
        if self.to_tensor:
            res_image = self.toTensor(image)
        return res_image

    
    