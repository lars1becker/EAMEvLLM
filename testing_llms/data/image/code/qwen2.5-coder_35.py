from PIL import Image

image_path = './data/image/ocean.jpg'
with Image.open(image_path) as img:
    file_format = img.format
    dimensions = img.size
    width, height = dimensions
    aspect_ratio = width / height if height != 0 else float('inf')

result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}
print(result)