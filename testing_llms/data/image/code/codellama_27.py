import sys
from PIL import Image
from pathlib import Path

# Set the path to the image file
image_path = Path('./data/image/ocean.jpg')

# Load the image using Pillow
with Image.open(image_path) as im:
    # Get the file format of the image
    file_format = im.format
    
    # Get the dimensions of the image
    width, height = im.size
    
    # Calculate the aspect ratio of the image
    aspect_ratio = float(width)/height

# Create a dictionary to store the results
result = {
    'file_format': file_format,
    'dimensions': f'{width}x{height}',
    'aspect_ratio': str(aspect_ratio)
}

print(result)