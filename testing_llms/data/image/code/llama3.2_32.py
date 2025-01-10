import os
from PIL import Image

result = {
    'file_format': os.path.splitext(os.path.basename('ocean.jpg'))[1],
    'dimensions': (os.path.getsize('ocean.jpg'), os.path.getsize('ocean.jpg') / 2),
    'aspect_ratio': os.popen('identify -format "%w %h" ocean.jpg').read()
}
print(result)