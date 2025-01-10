import PIL
from PIL import Image

image = Image.open('./data/image/ocean.jpg')
result = {}

# get image format
result['file_format'] = image.format

# get image dimensions
width, height = image.size
result['dimensions'] = f'{width}x{height}'

# get image aspect ratio
result['aspect_ratio'] = width / height

print(result)