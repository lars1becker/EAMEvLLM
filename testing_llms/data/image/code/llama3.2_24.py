from PIL import Image
import os

def get_image_info(image_path):
    image = Image.open(image_path)
    file_format = image.format
    dimensions = (image.size)
    aspect_ratio = None
    if dimensions[1] > dimensions[0]:
        aspect_ratio = dimensions[1] / dimensions[0]
    elif dimensions[0] > dimensions[1]:
        aspect_ratio = dimensions[0] / dimensions[1]
    
    result = {
        'file_format': file_format,
        'dimensions': str(dimensions),
        'aspect_ratio': aspect_ratio
    }
    return result

result = get_image_info('./data/image/ocean.jpg')
print(result)