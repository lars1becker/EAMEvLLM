import imghdr
import pyexiv2

def get_image_info(image_path):
    result = {}
    try:
        file_format = imghdr.what(image_path)
        dimensions = (pyexiv2.Image(image_path).height, pyexiv2.Image(image_path).width)
        aspect_ratio = dimensions[0] / dimensions[1]
        result['file_format'] = file_format
        result['dimensions'] = str(dimensions)
        result['aspect_ratio'] = str(aspect_ratio)
    except Exception as e:
        print(f"Error processing image: {e}")
    return result

image_path = './data/image/ocean.jpg'
result = get_image_info(image_path)
print(result)