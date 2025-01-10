from PIL import Image

# Open the image file
with Image.open('./data/image/ocean.jpg') as img:
    # Extract file format
    file_format = img.format
    
    # Extract dimensions
    dimensions = img.size
    
    # Calculate aspect ratio
    width, height = dimensions
    aspect_ratio = width / height
    
    # Save the results to a dictionary
    result = {
        'file_format': file_format,
        'dimensions': dimensions,
        'aspect_ratio': aspect_ratio
    }

# Print the result
print(result)