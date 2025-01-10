from PIL import Image
import os

# Open image file using PIL library
image = Image.open('./data/image/ocean.jpg')

# Get image format
file_format = image.format

# Get image dimensions
dimensions = image.size
width, height = dimensions

# Calculate aspect ratio
aspect_ratio = width / height

result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

print(result)