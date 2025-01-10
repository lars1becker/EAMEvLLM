import PIL.Image

# Open image file using Pillow
with open('./data/image/ocean.jpg', 'rb') as f:
    image = Image.open(f)

# Extract file format and dimensions
result = {
    'file_format': image.format,
    'dimensions': (image.width, image.height),
    'aspect_ratio': round(image.width / image.height, 2)
}

print(result)