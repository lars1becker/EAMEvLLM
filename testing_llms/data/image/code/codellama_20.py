import os
from PIL import Image

# Get the absolute path of the image file
image_path = os.path.abspath(os.path.join(os.getcwd(), './data/image/ocean.jpg'))

# Open the image using Pillow's Image class
with Image.open(image_path) as image:
    # Get the file format of the image
    file_format = image.format
    
    # Get the dimensions of the image (width and height)
    width, height = image.size
    
    # Calculate the aspect ratio of the image (width / height)
    aspect_ratio = width / height
    
# Create a dictionary to store the result
result = {
    'file_format': file_format,
    'dimensions': f'{width}x{height}',
    'aspect_ratio': round(aspect_ratio, 2)
}

print(result)