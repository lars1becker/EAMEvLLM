import os
from PIL import Image

result = {
    'file_format': os.path.splitext(os.path.basename('./data/image/ocean.jpg'))[1],
    'dimensions': (os.popen('identify -format "%wx%h" ./data/image/ocean.jpg').read().strip()),
    'aspect_ratio': (os.popen('identify -format "%w:%h" ./data/image/ocean.jpg').read().strip())
}

print(result)