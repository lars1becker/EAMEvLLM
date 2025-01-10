import os
from PIL import Image

def main():
    image_path = "./data/image/ocean.jpg"
    with Image.open(image_path) as image:
        file_format = os.path.splitext(image_path)[1][1:]
        dimensions = (image.width, image.height)
        aspect_ratio = float(dimensions[0]) / dimensions[1]
    result = {
        'file_format': file_format,
        'dimensions': dimensions,
        'aspect_ratio': aspect_ratio
    }
    print(result)

if __name__ == "__main__":
    main()