import os

def get_image_info(image_path):
    result = {}
    
    file_format = os.path.splitext(os.path.basename(image_path))[1]
    dimensions = (os.path.getsize(image_path) / 1024, os.path.getsize(image_path) / 1024)
    aspect_ratio = None
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
        
        width, height = image_data[0:2]
        ratio = width / height
        
        if width > height and ratio != float('inf'):
            aspect_ratio = f"{width}:{height}"
        elif height > width and ratio != 1:
            aspect_ratio = f"{height}:{width}"
        else:
            aspect_ratio = "unknown"
    
    result['file_format'] = file_format
    result['dimensions'] = str(dimensions)
    result['aspect_ratio'] = aspect_ratio
    
    return result

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)

print(result)