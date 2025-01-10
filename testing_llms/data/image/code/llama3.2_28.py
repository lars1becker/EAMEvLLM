import os

def extract_image_info(file_path):
    result = {}
    
    # Extract file format
    file_format = os.path.splitext(file_path)[1].lower()
    result['file_format'] = file_format
    
    # Check if image dimensions can be determined using EXIF data
    import exifread
    try:
        with open(file_path, 'rb') as file:
            tags = exifread.process_file(file)
            dimensions = tags.get('ImageWidth', None) or tags.get('ImageHeight', None)
            aspect_ratio = f"{int(dimensions)}:{tags['ImageExif']['FNumber'].split('.')[0]}"
            result['dimensions'] = f"{dimensions} x {aspect_ratio}"
    except FileNotFoundError:
        pass
    
    # Check if image dimensions can be determined using a pixel density file
    import glob
    files = glob.glob(f"*.ppm ./data/image/?.ppm")
    if len(files) > 0:
        result['pixel_density'] = f"{os.path.getsize('./data/image') / os.path.getsize(files[0])}"
    
    return result

result = extract_image_info('./data/image/ocean.jpg')
print(result)