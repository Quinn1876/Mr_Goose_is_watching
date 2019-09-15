from PIL import Image

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
                
def imgComposition(meme, face, top, left):
    # Top Left is the location on the meme where the face goes
    # Both meme and face should be pillow objects
    if not type(meme) is Image.Image or not type(face) is Image.Image:
        raise Exception
    
    # get the correct size
    x, y = face.size
    meme.paste(face, (top,left,top+x,left+y))
    return meme

def take_photo():

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(os.path.join(os.path.dirname(os.path.realpath(__file__)) + "/UserPhotos" , img_name), frame)
            print("{} written!".format(img_name))
            img_counter += 1
            break

    cam.release()

    cv2.destroyAllWindows()

def cropImage(meme_path, top, left, height, width):
    img = Image.open(meme_path)
    area = (top, left, top+height, left+width)
    cropped_img = img.crop(area)
    return cropped_img

