import PIL
from PIL import Image

img = Image.open('./data/image/ocean.jpg')
file_format = img.format
dimensions = img.size
aspect_ratio = img.width / img.height
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}
print(result)