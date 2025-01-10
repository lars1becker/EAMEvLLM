import os
from PIL import Image

def get_image_info(image_path):
    image = Image.open(image_path)
    result = {}
    result['file_format'] = image.format
    result['dimensions'] = (image.width, image.height)
    result['aspect_ratio'] = round(image.size[0]/image.size[1], 2)
    return result

result = get_image_info('./data/image/ocean.jpg')
print(result)