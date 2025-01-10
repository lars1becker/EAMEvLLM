import os
from PIL import Image

# Open the image using PIL
im = Image.open('./data/image/ocean.jpg')

# Get the file format
file_format = im.format

# Get the dimensions of the image
dimensions = str(im.size)

# Calculate the aspect ratio (width / height)
aspect_ratio = float(im.width)/float(im.height)

# Create a dictionary to store the results
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

# Print the results
print(result)