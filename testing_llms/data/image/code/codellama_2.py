import os
from PIL import Image
import numpy as np

# path to the image file
image_path = './data/image/ocean.jpg'

# read the image using PIL library
img = Image.open(image_path)

# extract the file format of the image
file_format = img.format

# extract the dimensions (width and height) of the image
dimensions = np.array(img.size)

# calculate the aspect ratio of the image
aspect_ratio = float(dimensions[0]) / dimensions[1]

# save the results to a dictionary
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

# print the result
print(result)