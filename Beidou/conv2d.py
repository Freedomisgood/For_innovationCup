# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 20:15:18 2018
@author: wmy
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class ObstacleDetection():
    '''
    example 1:
        
        od = ObstacleDetection()
        od.run('img.jpg')
        
    example 2:
        
        od = ObstacleDetection()
        kernel = od.creat_kernel_3x3()
        img = od.open_image('img.jpg')
        img = od.conv2d_3x3(img, kernel)
        warning_pixes_index = od.check(img)
        if len(warning_pixes_index)==0:
            print('ok!')
        else:
            print('warning!')
    '''
    
    def __init__(self):
        pass
    
    def creat_kernel_3x3(self):
        kernel = np.array([[-2,  2, -2], 
                           [ 2,  0,  2], 
                           [-2,  2, -2]])
        return kernel

    def open_image(self, path, size=(256, 256)):
        img = Image.open(path)
        img = img.resize(size)
        img = np.array(img)
        return img 

    def conv2d_3x3(self, img, kernel):
        h, w, c = img.shape
        output = []
        for m in range(1, h-1):
            output.append([])
            for n in range(1, w-1):
                pix = kernel[0][0] * img[m-1][n-1] + \
                kernel[0][1] * img[m-1][n] + \
                kernel[0][2] * img[m-1][n+1] + \
                kernel[1][0] * img[m][n-1] + \
                kernel[1][1] * img[m][n] + \
                kernel[1][2] * img[m][n+1] + \
                kernel[2][0] * img[m+1][n-1] + \
                kernel[2][1] * img[m+1][n] + \
                kernel[2][2] * img[m+1][n+1]
                output[m-1].append(pix)
                pass
            pass
        return output            
  
    def check(self, img, threshold=64, draw=False):
        warning_pixes_index = []
        y1 = int(len(img)*0.7)
        y2 = int(len(img))
        x1 = int(len(img[0])*0.15)
        x2 = int(len(img[0])*0.85)
        copy = np.copy(img)
        for m in range(y1, y2):
            for n in range(x1, x2):
                if img[m][n][0] > threshold or img[m][n][1] > threshold \
                or img[m][n][2] > threshold:
                    warning_pixes_index.append((m, n))
                    copy[m][n] = [255, 0, 0]
                    pass
                pass
            pass
        if draw:
            for n in range(x1, x2):
                copy[y1-1][n] = [0, 0, 255]
                copy[y2-1][n] = [0, 0, 255]
                pass
            for m in range(y1, y2):
                copy[m][x1-1] = [0, 0, 255]
                copy[m][x2-1] = [0, 0, 255]
                pass
            plt.imshow(copy)
            plt.show()
            pass
        return warning_pixes_index


    def run(self, img_path):
        kernel = self.creat_kernel_3x3()
        img = self.open_image(img_path)
        img = self.conv2d_3x3(img, kernel)
        warning_pixes_index = self.check(img)
        if len(warning_pixes_index)==0:
            return True
        else:
            return False
        pass
    
    pass
    