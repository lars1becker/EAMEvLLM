import cv2
from PIL import Image

def get_image_properties(image_path):
    image = cv2.imread(image_path)
    result = {
        'file_format': cv2.getFormatName(image.mode),
        'dimensions': f"{image.shape[1]}x{image.shape[0]}",
        'aspect_ratio': image.shape[1] / image.shape[0]
    }
    return result

print(get_image_properties('./data/image/ocean.jpg'))