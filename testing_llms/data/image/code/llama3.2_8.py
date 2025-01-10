import PIL
from PIL import Image

def get_image_info(file_path):
    image = Image.open(file_path)
    result = {
        'file_format': image.format,
        'dimensions': str(image.size),
        'aspect_ratio': f"{image.width}/{image.height}"
    }
    return result

result = get_image_info('./data/image/ocean.jpg')
print(result)