import os
from PIL import Image

# Open the image file
with open('./data/image/ocean.jpg', 'rb') as f:
    # Load the image using the Pillow library
    im = Image.open(f)
    
    # Get the file format of the image
    file_format = os.path.splitext(os.path.basename(im.filename))[1]
    
    # Get the dimensions of the image
    width, height = im.size
    
    # Calculate the aspect ratio of the image
    aspect_ratio = float(width) / float(height)
    
# Save the results to a dictionary
result = {
    'file_format': file_format,
    'dimensions': (width, height),
    'aspect_ratio': aspect_ratio
}

print(result)