import cv2
img = cv2.imread("./data/image/ocean.jpg")
dimensions = img.shape[:2] # shape of the image (width, height)
file_format = cv2.VideoCapture(0).get(cv2.CAP_PROP_FOURCC) # file format is JPG
aspect_ratio = dimensions[1] / dimensions[0]
result = {
    'file_format': file_format,
    'dimensions': dimensions,
    'aspect_ratio': aspect_ratio
}
print(result)