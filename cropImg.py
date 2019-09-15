from PIL import Image
filename = files[0] # replace as needed
from PIL import Image

def cropImage(file_path, top, left, height, width):
    img = Image.open(file_path)
    area = (top, left, top+height, left+width)
    cropped_img = img.crop(area)
    return cropped_img

def resizeImg(img, size:tuple)
    if len(size) != 2:
        raise Exception('size must have 2 items')
    for infile in sys.argv[1:]:
        outfile = os.path.splitext(infile)[0] + ".thumbnail"
        if infile != outfile:
            try:
                im = Image.open(infile)
                im.thumbnail(size, Image.ANTIALIAS)
                return im
            except IOError:
                print "cannot resize '%s'" % infile
                
def imgComposition(meme, face top, left):
    # Top Left is the location on the meme where the face goes
    
    # get the correct size
    x, y = face.size
    meme.paste(face, (top,left,top+x,left+y))
    return meme
