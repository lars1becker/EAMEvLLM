import os
from PIL import Image

def get_image_info(path):
    """
    Extracts file format, dimensions and aspect ratio of an image.

    Parameters:
        path (str): Path to the image file.

    Returns:
        result (dict): Dictionary containing file format, dimensions and aspect ratio of the image.
    """
    # Open the image using PIL's Image class
    image = Image.open(path)

    # Get the file format
    file_format = os.path.splitext(path)[1]

    # Get the dimensions (width and height) of the image
    width, height = image.size

    # Calculate the aspect ratio (width / height)
    aspect_ratio = width / height

    # Create a dictionary to store the result
    result = {
        'file_format': file_format,
        'dimensions': f'{width}x{height}',
        'aspect_ratio': f'{aspect_ratio:.2f}'
    }

    return result

# Test the function with a sample image
result = get_image_info('./data/image/ocean.jpg')
print(result)
```