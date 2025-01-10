import os
from PIL import Image

def extract_image_info(path):
    # Open the image using the Python Imaging Library (PIL)
    with Image.open(path) as image:
        # Get the file format of the image
        file_format = image.format
        
        # Get the dimensions of the image
        width, height = image.size
        
        # Calculate the aspect ratio of the image (width / height)
        aspect_ratio = float(width) / float(height)
    
    # Create a dictionary to store the extracted information
    result = {
        'file_format': file_format,
        'dimensions': f'{width} x {height}',
        'aspect_ratio': aspect_ratio
    }
    
    return result

# Test the function with a sample image
result = extract_image_info('./data/image/ocean.jpg')
print(result)