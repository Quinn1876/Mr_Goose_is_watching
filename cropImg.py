from PIL import Image
filename = files[0] # replace as needed
from PIL import Image

def cropImage(relativeFilePath, top, left, height, width):
    img = Image.open('memes\\'+filename)
    area = (top, left, top+height, left+width)
    cropped_img = img.crop(area)
    return cropped_img
