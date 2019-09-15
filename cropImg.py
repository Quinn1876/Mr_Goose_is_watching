from PIL import Image
filename = files[0] # replace as needed
from PIL import Image

def cropImage(file_path, top, left, height, width):
    img = Image.open(file_path)
    area = (top, left, top+height, left+width)
    cropped_img = img.crop(area)
    return cropped_img
