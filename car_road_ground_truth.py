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
if os.path.exists(car_seg_folder):
    shutil.rmtree(car_seg_folder)
os.makedirs(car_seg_folder)

road_seg_folder = os.path.dirname(seg_folder) + '/' + road_seg_folder
if os.path.exists(road_seg_folder):
    shutil.rmtree(road_seg_folder)
os.makedirs(road_seg_folder)

image_files = glob.glob(seg_folder + '/*.png')
for image_file in image_files:
    image = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2RGB)
    # Ignore car pixels after row 490
    red490 = image[490:,:,0]
    red490[red490 == 10] = 0
    # Grab red channel
    red = image[:,:,0,np.newaxis]
    # Look for cars
    car_image = np.where(red == 10, [255, 255, 255], [0, 0, 0])
    # Save car image
    cv2.imwrite(car_seg_folder + '/' + os.path.basename(image_file), car_image)
    # Look for roads
    road_image = np.where(np.logical_or(red == 6, red == 7), [255, 255, 255], [0, 0, 0])
    # Save road image
    cv2.imwrite(road_seg_folder + '/' + os.path.basename(image_file), road_image)
