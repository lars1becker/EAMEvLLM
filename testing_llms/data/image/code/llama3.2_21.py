import os
from PIL import Image

result = {}

def get_image_info(image_path):
    file_format = ImageFormat(image_path).filename.split('.')[-1]
    image_data = Image.open(image_path).data
    
    width, height = image_data.shape[:2]
    
    aspect_ratio = width / height
    
    result['file_format'] = file_format
    result['dimensions'] = f"{width}x{height}"
    result['aspect_ratio'] = str(aspect_ratio)

def main():
    global result
    get_image_info('./data/image/ocean.jpg')
    print(result)

main()