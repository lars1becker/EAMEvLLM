import PIL
from PIL import Image
image = Image.open("./data/image/ocean.jpg")
result = {
    'file_format': image.format,
    'dimensions': (image.width, image.height),
    'aspect_ratio': image.width / image.height
}
print(result)