import os
from PIL import Image

# path to the image file
img_path = './data/image/ocean.jpg'

# open the image using Pillow
with open(img_path, 'rb') as f:
    img = Image.open(f)

# get the file format of the image
file_format = img.format

# get the dimensions (width and height) of the image
dimensions = img.size

# calculate the aspect ratio of the image
aspect_ratio = float(dimensions[0]) / dimensions[1]

# save the result to a dictionary
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

print(result)