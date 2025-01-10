import os
from PIL import Image

image_path = "./data/image/ocean.jpg"

if not os.path.exists(image_path):
    print("File does not exist")
    exit()

# Open the image file using Pillow
with Image.open(image_path) as image:
    # Get the file format of the image
    file_format = image.format
    
    # Get the dimensions of the image
    width, height = image.size
    
    # Calculate the aspect ratio of the image
    aspect_ratio = width / height

result = {
    'file_format': file_format,
    'dimensions': (width, height),
    'aspect_ratio': aspect_ratio
}

print(result)