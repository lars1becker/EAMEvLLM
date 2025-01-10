import os
from PIL import Image

def get_image_info(image_path):
    """
    Extracts information about an image file.
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        dict: A dictionary containing information about the image, with keys for 'file_format', 'dimensions' and 'aspect_ratio'.
    """
    
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Get the file format of the image
    file_format = os.path.splitext(image_path)[1]
    
    # Get the dimensions of the image
    width, height = image.size
    
    # Calculate the aspect ratio of the image
    aspect_ratio = width / height
    
    # Save the information to a dictionary
    result = {
        'file_format': file_format,
        'dimensions': (width, height),
        'aspect_ratio': aspect_ratio
    }
    
    return result

# Test the function
result = get_image_info('./data/image/ocean.jpg')
print(result)