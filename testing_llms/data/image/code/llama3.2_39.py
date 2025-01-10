import imghdr
from PIL import Image

def get_image_info(image_path):
    file_format = imghdr.what(image_path)
    image_data = open(image_path, 'rb').read()
    width, height, channels = image_data[:3]
    aspect_ratio = float(width) / float(height)
    dimensions = (width, height)
    return {
        'file_format': file_format,
        'dimensions': dimensions,
        'aspect_ratio': str(aspect_ratio)
    }

result = get_image_info('./data/image/ocean.jpg')
print(result)