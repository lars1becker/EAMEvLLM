import os
from PIL import Image

image_path = "./data/image/ocean.jpg"

if not os.path.exists(image_path):
    raise ValueError("Image file does not exist")

with Image.open(image_path) as image:
    result = {
        'file_format': image.format,
        'dimensions': (image.width, image.height),
        'aspect_ratio': image.width / image.height
    }

print(result)