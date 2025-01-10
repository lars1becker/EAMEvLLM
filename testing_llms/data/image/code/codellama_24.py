import os
from PIL import Image

image_path = "./data/image/ocean.jpg"

# Open the image file using PIL
with Image.open(image_path) as im:
    # Get the file format of the image
    file_format = im.format
    
    # Get the dimensions of the image (width and height)
    dimensions = im.size
    
    # Calculate the aspect ratio of the image (width / height)
    aspect_ratio = dimensions[0] / dimensions[1]

# Create a dictionary to store the results
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

print(result)