import os

def get_image_info(image_path):
    result = {}
    
    file_format = os.path.splitext(os.path.basename(image_path))[1]
    dimensions = (int(os.popen('identify -format "%w x %h" /dev/stdin').read().splitlines()[0]), int(os.popen('identify -format "%w x %h" /dev/stdin').read().splitlines()[1]))
    aspect_ratio = f"{dimensions[0]}/{dimensions[1]}"
    
    result['file_format'] = file_format
    result['dimensions'] = dimensions
    result['aspect_ratio'] = aspect_ratio
    
    return result

image_path = './data/image/ocean.jpg'
print(get_image_info(image_path))