import os
from PIL import Image

image_path = "./data/image/ocean.jpg"

def get_image_properties(image_path):
    image = Image.open(image_path)
    
    # Get the file format of the image
    file_format = os.path.splitext(image_path)[1]
    
    # Get the dimensions of the image
    width, height = image.size
    
    # Calculate the aspect ratio of the image
    aspect_ratio = float(width)/float(height)
    
    return {
        'file_format': file_format,
        'dimensions': (width, height),
        'aspect_ratio': aspect_ratio
    }

result = get_image_properties(image_path)
print(result)