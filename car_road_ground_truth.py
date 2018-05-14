#!/usr/bin/python

import os
import sys
import glob
import shutil
import numpy as np
import cv2

car_seg_folder = 'CarSeg'
road_seg_folder = 'RoadSeg'

if len(sys.argv) < 2:
    print('Please enter the folder path.')
    sys.exit()

seg_folder = os.path.abspath(sys.argv[1])
if not os.path.isdir(seg_folder):
    print('Please enter a valid folder path')
    sys.exit()

car_seg_folder = os.path.dirname(seg_folder) + '/' + car_seg_folder
shutil.rmtree(car_seg_folder)
os.makedirs(car_seg_folder)
road_seg_folder = os.path.dirname(seg_folder) + '/' + road_seg_folder
shutil.rmtree(road_seg_folder)
os.makedirs(road_seg_folder)

image_files = glob.glob(seg_folder + '/*.png')
for image_file in image_files:
    image = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2RGB)
    # Grab red channel
    red = image[:,:,0]
    red = np.expand_dims(red, axis=2)
    # Look for cars
    car_image = np.where((red == 10).all(), np.ones(red.shape[:-1] + (3,)) * 255, np.ones(red.shape[:-1] + (3,)))
    #print(car_image.shape)
    #print((np.ones(red.shape[:-1] + (3,)) * 255).shape)
    # Save car image
    cv2.imwrite(car_seg_folder + '/' + os.path.basename(image_file), car_image)
    # Look for roads
    road_image = np.where((red == 6).all() or (red == 7).all(), np.ones(red.shape[:-1] + (3,)) * 255, np.ones(red.shape[:-1] + (3,)))
    # Save road image
    cv2.imwrite(road_seg_folder + '/' + os.path.basename(image_file), road_image)
