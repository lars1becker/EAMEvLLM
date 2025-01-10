import os
from PIL import Image

# Set the path to the image file
image_path = './data/image/ocean.jpg'

# Open the image using Pillow library
with open(image_path, 'rb') as f:
    image = Image.open(f)

# Get the file format
file_format = os.path.splitext(image_path)[1][1:]

# Get the dimensions of the image
width, height = image.size

# Calculate the aspect ratio of the image
aspect_ratio = width / height

# Save the results to a dictionary
result = {
    'file_format': file_format,
    'dimensions': f'{width}x{height}',
    'aspect_ratio': aspect_ratio
}

print(result)