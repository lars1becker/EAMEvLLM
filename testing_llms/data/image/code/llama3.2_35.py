import os
from PIL import Image

def get_image_info(image_path):
    image = Image.open(image_path)
    file_format = image.format
    dimensions = (image.size[0], image.size[1])
    aspect_ratio = image.width / image.height
    return {
        'file_format': file_format,
        'dimensions': str(dimensions),
        'aspect_ratio': str(aspect_ratio)
    }

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)

print(result)