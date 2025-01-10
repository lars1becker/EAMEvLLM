import os
from PIL import Image

image_path = './data/image/ocean.jpg'

with open(image_path, 'rb') as f:
    image = Image.open(f)
    file_format = image.format
    dimensions = (image.width, image.height)
    aspect_ratio = dimensions[0] / dimensions[1]

result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}
print(result)