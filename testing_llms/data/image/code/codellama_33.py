import os
from PIL import Image

def get_image_info(path):
    image = Image.open(path)
    file_format = os.path.splitext(path)[1][1:]
    dimensions = (image.width, image.height)
    aspect_ratio = round(image.width / image.height, 2)
    return {'file_format': file_format, 'dimensions': dimensions, 'aspect_ratio': aspect_ratio}

path = './data/image/ocean.jpg'
result = get_image_info(path)
print(result)