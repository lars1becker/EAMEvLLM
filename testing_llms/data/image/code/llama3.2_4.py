import os

def get_image_info(image_path):
    result = {}

    # Get file format
    file_format = os.path.splitext(os.path.basename(image_path))[1].lower()
    result['file_format'] = file_format

    # Get image dimensions
    image_data = open(image_path, 'rb').read()
    width, height = struct.unpack('HH', image_data)
    result['dimensions'] = f'{width}x{height}'

    # Get image aspect ratio
    image_data = open(image_path, 'r+b').read()
    image_width, _ = struct.unpack('HH', image_data[:2])
    image_height = height
    if image_width == 0:
        image_aspect_ratio = float('inf')
    else:
        image_aspect_ratio = (image_width / image_height) if image_height != 0 else float('inf')

    result['aspect_ratio'] = str(image_aspect_ratio)

    return result

result = get_image_info('./data/image/ocean.jpg')
print(result)