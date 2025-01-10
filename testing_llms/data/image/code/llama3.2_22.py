import os

def extract_image_info(image_path):
    result = {}
    dimensions = None
    aspect_ratio = None
    
    # Get file format from image extension
    file_extension = os.path.splitext(os.path.basename(image_path))[1]
    if file_extension.lower() == '.jpg' or file_extension.lower() == '.jpeg':
        result['file_format'] = 'image'
    elif file_extension.lower() in ['.png', '.gif']:
        result['file_format'] = 'image'
    
    # Get image dimensions
    image_file = os.path.splitext(os.path.basename(image_path))[0]
    with open(image_file, 'r') as f:
        for line in f:
            if b'width=' in line or b'height=' in line:
                width = int(line.split(b'width=')[1].split('=')[1])
                height = int(line.split(b'height=')[1].split('=')[1])
                dimensions = (width, height)
                break
    result['dimensions'] = f'{width}x{height}'
    
    # Get image aspect ratio
    with open(image_file, 'r') as f:
        for line in f:
            if b'width=' in line or b'height=' in line:
                width = int(line.split(b'width=')[1].split('=')[1])
                height = int(line.split(b'height=')[1].split('=')[1])
                aspect_ratio = str(width / float(height))
                break
    result['aspect_ratio'] = f'{width}/{height}'
    
    return result

image_path = './data/image/ocean.jpg'
result = extract_image_info(image_path)
print(result)