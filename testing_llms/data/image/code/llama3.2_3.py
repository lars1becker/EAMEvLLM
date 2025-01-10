import os

def get_image_info(image_path):
    image_name = os.path.basename(image_path)
    file_format = image_name.split('.')[-1]
    dimensions = tuple(map(int, open(image_path).readline().split()))
    aspect_ratio = dimensions[0] / dimensions[1]

    result = {
        'file_format': file_format,
        'dimensions': str(dimensions),
        'aspect_ratio': aspect_ratio
    }

    return result

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)
print(result)