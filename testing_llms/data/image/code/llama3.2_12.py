import cv2
import numpy as np

def extract_image_info(image_path):
    img = cv2.imread(image_path)
    file_format = img.format
    dimensions = img.size
    aspect_ratio = None
    if len(dimensions) > 1:
        height, width, _ = dimensions
        aspect_ratio = width / height
    
    result = {
        'file_format': file_format,
        'dimensions': str(width) + "x" + str(height),
        'aspect_ratio': aspect_ratio if not isinstance(aspect_ratio, float) else aspect_ratio
    }
    
    return result

result = extract_image_info('./data/image/ocean.jpg')
print(result)