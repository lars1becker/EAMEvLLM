import imghdr
from PIL import Image

def get_image_info(image_path):
    result = {
        'file_format': imghdr.what(image_path),
        'dimensions': (Image.open(image_path).size[0], Image.open(image_path).size[1]),
        'aspect_ratio': str(Image.open(image_path).width / Image.open(image_path).height)
    }
    return result

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)
print(result)