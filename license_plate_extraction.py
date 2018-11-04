# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.


"""
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import numpy as np
from skimage.transform import resize
from skimage import io
import os
import time

class extraction():
    def __init__(self):
        pass
    
    def store_license_plate(image_path,save_path):



        
        car_image = imread(image_path, as_grey=True)
        original = imread(image_path, as_grey=False)
# it should be a 2 dimensional array
        print(car_image.shape)

# the next line is not compulsory however, a grey scale pixel
# in skimage ranges between 0 & 1. multiplying it with 255
# will make it range between 0 & 255 (something we can relate better with

        gray_car_image = car_image * 255
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(gray_car_image, cmap="gray")
        threshold_value = threshold_otsu(gray_car_image)
        binary_car_image = gray_car_image > threshold_value
        ax2.imshow(binary_car_image, cmap="gray")
        plt.show()
        
        label_image = measure.label(binary_car_image)
        
        # getting the maximum width, height and minimum width and height that a license plate can be
        plate_dimensions = (0.04*label_image.shape[0], 0.2*label_image.shape[0], 0.1*label_image.shape[1], 0.4*label_image.shape[1])
        min_height, max_height, min_width, max_width = plate_dimensions
        plate_objects_cordinates = []
        plate_like_objects = []
        fig, (ax1) = plt.subplots(1)
        ax1.imshow(gray_car_image, cmap="gray");
        
        # regionprops creates a list of properties of all the labelled regions
        for region in regionprops(label_image):
            if region.area < 50:
                #if the region is so small then it's likely not a license plate
                continue
        
            # the bounding box coordinates
            min_row, min_col, max_row, max_col = region.bbox
            region_height = max_row - min_row
            region_width = max_col - min_col
            # ensuring that the region identified satisfies the condition of a typical license plate
            if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
                plate_like_objects.append(binary_car_image[min_row:max_row,
                                          min_col:max_col])
                plate_objects_cordinates.append([min_row, min_col,
                                                      max_row, max_col])
                rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
                ax1.add_patch(rectBorder)
            # let's draw a red rectangle over those regions
        plt.show()
        
        # we use the same method to segment each character in each candidate, if we can label more than five characters, it should be the license plate.
        count = 0
        for each_candidate in plate_like_objects:
            each_candidate = np.invert(each_candidate)
            labelled_candidate = measure.label(each_candidate)
            character_dimensions = (0.1*each_candidate.shape[0], 0.9*each_candidate.shape[0], 0.02*each_candidate.shape[1], 0.2*each_candidate.shape[1])
            min_height, max_height, min_width, max_width = character_dimensions
            characters = []
            for regions in regionprops(labelled_candidate):
                y0, x0, y1, x1 = regions.bbox
                region_height = y1 - y0
                region_width = x1 - x0
                    
                if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
                     roi = each_candidate[y0:y1, x0:x1]
                     resized_char = resize(roi, (20, 20))
                     characters.append(resized_char)
            if len(characters) > 5:
                break
            count +=1
        y0 = plate_objects_cordinates[count][0]
        x0 = plate_objects_cordinates[count][1]
        y1 = plate_objects_cordinates[count][2]
        x1 = plate_objects_cordinates[count][3]
        license_plate=original[y0:y1, x0:x1]  
        license_plate= resize(license_plate, (161, 314))       
        
        
        io.imsave(save_path,license_plate)
    
    def time_extraction(file_path):
        
        t = os.path.getctime(file_path)
        timeStruct = time.localtime(t)
        return(time.strftime('%Y-%m-%d %H:%M:%S',timeStruct))



