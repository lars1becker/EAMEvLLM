import PIL
from PIL import Image

def extract_image_info(image_path):
    with Image.open(image_path) as img:
        result = {
            'file_format': img.format,
            'dimensions': (img.width, img.height),
            'aspect_ratio': img.width / img.height
        }
        print(result)

extract_image_info('./data/image/ocean.jpg')