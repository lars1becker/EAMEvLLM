from PIL import Image
import os

def get_image_info(image_path):
    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = image.width / image.height
    result = {
        'file_format': image.format,
        'dimensions': f'{width}x{height}',
        'aspect_ratio': str(aspect_ratio)
    }
    return result

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)

print(result)