import numpy as np
from PIL import Image

def get_image_info(image_path):
    img = Image.open(image_path)
    width, height = img.size
    aspect_ratio = width / height
    return {
        'file_format': img.format,
        'dimensions': f'{width}x{height}',
        'aspect_ratio': f'{aspect_ratio:.2f}'
    }

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)
print(result)