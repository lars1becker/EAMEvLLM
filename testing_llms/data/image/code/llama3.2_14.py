import os
from PIL import Image

def get_image_info(image_path):
    try:
        image = Image.open(image_path)
        file_format = image.format
        width, height = image.size
        aspect_ratio = (width / height) if width > height else float('inf')
        return {
            'file_format': file_format,
            'dimensions': f'{width}x{height}',
            'aspect_ratio': f'{aspect_ratio:.2f}'
        }
    except Exception as e:
        print(f"Error processing image: {e}")
        return {}

result = get_image_info('./data/image/ocean.jpg')
print(result)