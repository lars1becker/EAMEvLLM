import os
import PIL.Image

# Define path to image file
image_path = "./data/image/ocean.jpg"

# Open image using Pillow library
with open(image_path, 'rb') as f:
    image = PIL.Image.open(f)

# Extract image format
file_format = image.format

# Extract image dimensions (width and height)
dimensions = image.size

# Calculate aspect ratio (width / height)
aspect_ratio = float(dimensions[0]) / dimensions[1]

# Create dictionary to store results
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

print(result)