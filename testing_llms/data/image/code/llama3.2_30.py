import imghdr
from PIL import Image

def get_image_info(image_path):
    result = {}
    try:
        image_format = imghdr.what(image_path)
        dimensions = (Image.open(image_path).size[0], Image.open(image_path).size[1])
        aspect_ratio = dimensions[0] / dimensions[1]
        result['file_format'] = image_format
        result['dimensions'] = str(dimensions)
        result['aspect_ratio'] = str(aspect_ratio)
    except Exception as e:
        print(f"Error: {e}")
    return result

image_path = './data/image/ocean.jpg'
print(get_image_info(image_path))