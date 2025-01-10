import os
from PIL import Image

result = {}

def get_image_info(image_path):
    image = Image.open(image_path)

    file_format = image.format
    dimensions = (image.size)
    aspect_ratio = image.getaspectratio()

    result['file_format'] = file_format
    result['dimensions'] = str(dimensions[0]) + 'x' + str(dimensions[1])
    result['aspect_ratio'] = aspect_ratio

print(result)