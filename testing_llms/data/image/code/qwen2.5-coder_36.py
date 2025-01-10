from PIL import Image

image_path = './data/image/ocean.jpg'
with Image.open(image_path) as img:
    file_format = img.format
    dimensions = img.size
    aspect_ratio = dimensions[0] / dimensions[1]

result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}
print(result)