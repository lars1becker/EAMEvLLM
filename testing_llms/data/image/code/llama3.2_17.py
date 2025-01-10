import imghdr
from PIL import Image

def get_image_info(image_path):
    image = Image.open(image_path).convert('RGB')
    file_format = imghdr.what(image_path)
    dimensions = (image.size[0], image.size[1])
    aspect_ratio = image.size[1] / image.size[0]
    return {
        'file_format': file_format,
        'dimensions': str(dimensions),
        'aspect_ratio': str(aspect_ratio)
    }

result = get_image_info('./data/image/ocean.jpg')
print(result)