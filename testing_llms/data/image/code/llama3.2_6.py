import os

result = {}
image_file_path = './data/image/ocean.jpg'

# Read image file contents
with open(image_file_path, 'rb') as file:
    image_data = file.read()

# Extract file format
file_format = get_file_extension(file_data)
result['file_format'] = file_format

# Calculate image dimensions and aspect ratio
width, height = os.popen('identify -format "%w %h" %s').read().splitlines()[0].split()
aspect_ratio = width / height if height != 0 else float('inf')
result['dimensions'] = f'{width}x{height}'
result['aspect_ratio'] = aspect_ratio

print(result)