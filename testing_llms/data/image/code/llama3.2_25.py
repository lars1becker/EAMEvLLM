import os

def get_image_info(image_path):
    image_file_name = os.path.basename(image_path)
    file_format, image_extension = image_file_name.split('.')
    dimensions = None
    aspect_ratio = None

    if 'jpg' in image_extension:
        dimensions = (os.popen(f"identify -format '%[fx:width][!%w] %[cx] %[fy]" + image_path).read().splitlines()[0].strip())
    elif 'png' in image_extension:
        dimensions = (os.popen(f"convert {image_path} -format %[w] %[h]").read().splitlines()[0].strip() + ' 1')
    else:
        raise ValueError("Unsupported file format")

    aspect_ratio = image_file_name.split('.')[0]

    return {
        'file_format': file_format,
        'dimensions': dimensions,
        'aspect_ratio': aspect_ratio
    }

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)
print(result)