import os
import sys
from PIL import Image

FILE=""
if os.path.exists(FILE):
    pngfile=Image.open(FILE)
    jpgfile=pngfile.convert('RGB')
    jpgfile.save(FILE+".jpg")
    print("Success")
else:
    print(FILE+" not found!")
    