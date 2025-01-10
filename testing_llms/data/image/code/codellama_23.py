import PIL.Image
from PIL import ImageFile
image = Image.open("./data/image/ocean.jpg")
result = {
    'file_format': image.format,
    'dimensions': (image.width, image.height),
    'aspect_ratio': image.size[0] / image.size[1]
}
print(result)