import os
from PIL import Image

def get_image_info(image_path):
    image = Image.open(image_path)
    file_format = image.format.lower()
    dimensions = (image.size[0], image.size[1])
    aspect_ratio = image.size[1] / image.size[0]

    result = {
        'file_format': file_format,
        'dimensions': str(dimensions),
        'aspect_ratio': str(aspect_ratio)
    }
    return result

result = get_image_info('./data/image/ocean.jpg')
print(result)