import os
from PIL import Image

image_path = './data/image/ocean.jpg'

# Open the image file using PIL
with open(image_path, 'rb') as f:
    image = Image.open(f)

# Extract the file format
file_format = os.path.splitext(image_path)[-1]

# Calculate the aspect ratio and dimensions of the image
aspect_ratio = image.width / image.height
dimensions = (image.width, image.height)

# Save the result to a dictionary
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

print(result)