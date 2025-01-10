import PIL
from PIL import Image
img = Image.open('./data/image/ocean.jpg')
format = img.format
dimensions = f"{img.width} x {img.height}"
aspect_ratio = round(float(img.size[0]) / float(img.size[1]), 2)
result = {'file_format': format, 'dimensions': dimensions, 'aspect_ratio': aspect_ratio}
print(result)