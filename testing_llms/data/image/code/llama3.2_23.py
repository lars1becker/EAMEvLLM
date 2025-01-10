import os

def extract_image_info(image_path):
    result = {}
    image_format, file_extension = os.path.splitext(os.path.basename(image_path))
    
    # Determine dimensions based on image format
    if image_format.lower() == 'jpg':
        width = int(2**8 * 3**6 / (4 * 3.04))  # Assuming average JPEG compression ratio
        height = int((1 / 16) * width)
        
        # Calculate aspect ratio
        aspect_ratio = width / height
        
    elif image_format.lower() == 'png':
        width, height = map(int, os.popen(f'identify -format "%wx%h" {image_path}').readline().split())
        
        aspect_ratio = width / height
        
    else:
        raise ValueError(f"Unsupported image format: {image_format}")
    
    result['file_format'] = image_format
    result['dimensions'] = f'{width}x{height}'
    result['aspect_ratio'] = aspect_ratio
    
    return result

result = extract_image_info('./data/image/ocean.jpg')
print(result)