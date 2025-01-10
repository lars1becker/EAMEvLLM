import PIL
from PIL import Image

def get_image_info(path):
    with Image.open(path) as image:
        file_format = image.format
        dimensions = (image.width, image.height)
        aspect_ratio = float(image.width) / float(image.height)

        return {
            'file_format': file_format,
            'dimensions': dimensions,
            'aspect_ratio': aspect_ratio
        }

result = get_image_info('./data/image/ocean.jpg')
print(result)