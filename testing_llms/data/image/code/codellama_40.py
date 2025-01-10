import os 
from PIL import Image 

def get_image_details(image_path): 
    """ Get details of an image file """ 
  
    # Open the image using PIL 
    with open(image_path, 'rb') as f: 
        img = Image.open(f) 
  
    # Get the file format 
    file_format = os.path.splitext(image_path)[1][1:] 
  
    # Get the dimensions of the image 
    width, height = img.size 
  
    # Calculate the aspect ratio of the image 
    aspect_ratio = float(width) / height 
  
    return { 
        'file_format': file_format, 
        'dimensions': (width, height), 
        'aspect_ratio': aspect_ratio 
    }