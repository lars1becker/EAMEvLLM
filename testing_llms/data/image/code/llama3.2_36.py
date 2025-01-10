import os
from PIL import Image

def extract_image_info(image_path):
    image = Image.open(image_path)
    result = {
        'file_format': image.format,
        'dimensions': str(image.size),
        'aspect_ratio': f'{image.width}/{image.height}'
    }
    return result

result = extract_image_info('./data/image/ocean.jpg')
print(result)