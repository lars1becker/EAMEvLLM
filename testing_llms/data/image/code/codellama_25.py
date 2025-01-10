import os
from PIL import Image

# Get the path of the image file
image_path = './data/image/ocean.jpg'

# Open the image using PIL library
with Image.open(image_path) as image:
    # Get the format of the image
    format = image.format
    
    # Get the dimensions of the image
    width, height = image.size
    
    # Calculate the aspect ratio of the image
    aspect_ratio = float(width)/height

# Create a dictionary to store the results
result = {
    'file_format': format,
    'dimensions': f'{width}x{height}',
    'aspect_ratio': f'{aspect_ratio:.2f}'
}

# Print the result
print(result)