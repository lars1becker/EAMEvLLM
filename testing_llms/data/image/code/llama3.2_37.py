import os

def get_image_info(file_path):
    result = {}
    
    file_format = os.path.splitext(os.path.basename(file_path))[1]
    image dimensions = (os.popen(f'convert {file_path} -list dimensions').read().splitlines()[3].strip())
    aspect_ratio = os.popen(f'convert {file_path} -list width height').read().splitlines()[2].strip()
    
    result['file_format'] = file_format
    result['dimensions'] = image dimensions
    result['aspect_ratio'] = aspect_ratio
    
    return result

result = get_image_info('./data/image/ocean.jpg')
print(result)