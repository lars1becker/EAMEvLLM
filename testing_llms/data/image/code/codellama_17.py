import os
import sys
from PIL import Image

# Set the path to the image file
image_path = './data/image/ocean.jpg'

# Open the image using Pillow
with Image.open(image_path) as image:
    # Get the format of the image
    file_format = image.format

    # Get the dimensions of the image
    width, height = image.size

    # Calculate the aspect ratio of the image
    aspect_ratio = float(width) / height

# Create a dictionary to store the results
result = {
    'file_format': file_format,
    'dimensions': f'{width}x{height}',
    'aspect_ratio': f'{aspect_ratio:.2f}'
}

# Print out the results
print(result)