import numpy as np
from PIL import Image

def get_image_info(image_path):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    aspect_ratio = width / height
    dimensions = f'{width}x{height}'
    return {
        'file_format': type(img).__name__,
        'dimensions': dimensions,
        'aspect_ratio': aspect_ratio
    }

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)
print(result)