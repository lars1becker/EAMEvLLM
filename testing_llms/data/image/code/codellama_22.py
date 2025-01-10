import os
from PIL import Image

image_path = "./data/image/ocean.jpg"
image = Image.open(image_path)

result = {
    'file_format': image.format,
    'dimensions': f'{image.size[0]}x{image.size[1]}',
    'aspect_ratio': round(image.size[0] / image.size[1], 2) if image.size[0] > image.size[1] else round(image.size[1] / image.size[0], 2)
}
print(result)