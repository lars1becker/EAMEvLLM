import PIL
from PIL import Image

# Load the image using PIL
img = Image.open('./data/image/ocean.jpg')

# Get the file format of the image
file_format = img.format

# Get the dimensions of the image (width and height)
width, height = img.size

# Calculate the aspect ratio of the image (width / height)
aspect_ratio = width / height

# Save the results to a dictionary
result = {
    'file_format': file_format,
    'dimensions': f'{width}x{height}',
    'aspect_ratio': aspect_ratio
}

print(result)