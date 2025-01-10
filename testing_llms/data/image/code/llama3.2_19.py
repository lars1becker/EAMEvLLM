import imghdr
from PIL import Image

def get_image_properties(image_path):
    result = {}
    try:
        file_format, _ = imghdr.what(image_path)
        dimensions = tuple(Image.open(image_path).size)
        aspect_ratio = image_path.split('.')[-2].split('_')[-1]
        result['file_format'] = file_format
        result['dimensions'] = str(dimensions)
        result['aspect_ratio'] = aspect_ratio
    except Exception as e:
        print(f"Error processing image: {e}")
    return result

image_path = './data/image/ocean.jpg'
result = get_image_properties(image_path)
print(result)