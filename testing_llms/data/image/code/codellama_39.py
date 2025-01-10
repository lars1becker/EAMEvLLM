import PIL
from PIL import ImageFile

# Load the image
img = PIL.Image.open("./data/image/ocean.jpg")

# Get the file format of the image
file_format = img.format

# Get the dimensions (width and height) of the image
dimensions = img.size

# Calculate the aspect ratio of the image
aspect_ratio = float(dimensions[0]) / dimensions[1]

# Save the result to a dictionary
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}

print(result)