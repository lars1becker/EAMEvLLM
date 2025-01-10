import os

def get_image_info(image_path):
    image = Image.open(image_path)

    file_format = image.format
    dimensions = (image.size[0], image.size[1])
    aspect_ratio = image.size[1] / image.size[0]

    result = {
        'file_format': file_format,
        'dimensions': str(dimensions),
        'aspect_ratio': str(aspect_ratio)
    }

    return result

os.system('convert ./data/image/ocean.jpg info')
print(get_image_info('./data/image/ocean.jpg'))