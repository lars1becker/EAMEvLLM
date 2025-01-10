import os
from PIL import Image

# Get the path of the image file
image_path = './data/image/ocean.jpg'

# Open the image using the Python Imaging Library (PIL)
with Image.open(image_path) as image:
    # Get the file format of the image
    file_format = os.path.splitext(image_path)[1][1:]

    # Get the dimensions of the image
    dimensions = image.size

    # Calculate the aspect ratio of the image
    aspect_ratio = float(dimensions[0]) / float(dimensions[1])

# Create a dictionary to store the results
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

# Print the result
print(result)