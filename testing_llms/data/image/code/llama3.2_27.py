import os

def get_image_info(image_path):
    image_format = os.path.splitext(os.path.basename(image_path))[1].lower()
    dimensions = (os.popen(f"convert {image_path} -size +2+0x1000x2000 canvas none").read().strip())
    aspect_ratio = int(dimensions.split()[1:])
    
    return {
        'file_format': image_format,
        'dimensions': f'{dimensions}',
        'aspect_ratio': f'{aspect_ratio}'
    }

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)
print(result)