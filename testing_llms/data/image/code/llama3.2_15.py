import os
from PIL import Image

def get_image_info(image_path):
    try:
        img = Image.open(image_path)
        file_format = img.format.lower()
        dimensions = (img.size[0], img.size[1])
        aspect_ratio = dimensions[0] / dimensions[1]
        return {
            'file_format': file_format,
            'dimensions': str(dimensions),
            'aspect_ratio': str(aspect_ratio)
        }
    except Exception as e:
        print(f"Error: {e}")

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)

print(result)