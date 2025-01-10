import os
from PIL import Image

def get_image_info(filepath):
    image = Image.open(filepath)
    file_format = os.path.splitext(filepath)[1][1:]
    dimensions = (image.width, image.height)
    aspect_ratio = round(float(image.width) / float(image.height), 2)
    return {
        'file_format': file_format,
        'dimensions': dimensions,
        'aspect_ratio': aspect_ratio
    }

if __name__ == "__main__":
    result = get_image_info('./data/image/ocean.jpg')
    print(result)