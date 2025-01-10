import os
from PIL import Image

def get_image_info(image_path):
    file_format = image_path.split('.')[-1]
    dimensions = (Image.open(image_path).size)
    aspect_ratio = dimensions[0] / dimensions[1]

    return {
        'file_format': file_format,
        'dimensions': str(dimensions),
        'aspect_ratio': str(aspect_ratio)
    }

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)

print(result)