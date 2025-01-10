import os
from PIL import Image

def get_image_info(image_path):
    image = Image.open(image_path)
    result = {
        'file_format': image.format,
        'dimensions': (image.size[0], image.size[1]),
        'aspect_ratio': f"{image.size[0]}/{image.size[1]}"
    }
    return result

result = get_image_info('./data/image/ocean.jpg')
print(result)