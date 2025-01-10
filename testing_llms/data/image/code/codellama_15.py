import os
from PIL import Image

image_path = "./data/image/ocean.jpg"

# Open the image file using PIL's Image class
with open(image_path, 'rb') as f:
    image = Image.open(f)

# Extract the file format, dimensions and aspect ratio of the image
file_format = os.path.splitext(image_path)[1][1:]
dimensions = (image.width, image.height)
aspect_ratio = float(image.width)/float(image.height)

# Save the results to a dictionary
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

print(result)