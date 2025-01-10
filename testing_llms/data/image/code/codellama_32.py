from PIL import Image
import os

image_path = os.path.join('.', 'data', 'image', 'ocean.jpg')
with open(image_path, 'rb') as f:
    image = Image.open(f)

result = {
    'file_format': image.format,
    'dimensions': (image.width, image.height),
    'aspect_ratio': round(image.height / image.width, 2)
}
print(result)