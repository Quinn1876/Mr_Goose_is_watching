from PIL import Image
import os,sys
import cv2

def resizeImg(img, size:tuple):
    if len(size) != 2:
        raise Exception('size must have 2 items')
    try:
        im = img.resize(size, Image.NEAREST) #width,height
        return im
    except IOError:
        print ("cannot resize %s" % (img))
                
def imgComposition(meme, face, top, left):
    # Top Left is the location on the meme where the face goes
    # Both meme and face should be pillow objects
    # if not type(meme) is Image.Image or not type(face) is Image.Image:
    #     raise Exception
    
    # get the correct size
    width, height = face.size
    meme.paste(face, (left,top,left+width,top+height), face)
    return meme

def take_photo(photoCount):

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("SMILE FOR THE CAMERA :)")

    while True:
        ret, frame = cam.read()
        cv2.imshow("SMILE FOR THE CAMERA :)", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(photoCount)
            cv2.imwrite(os.path.join(os.path.dirname(os.path.realpath(__file__)) + "/UserPhotos" , img_name), frame)
            print("{} written!".format(img_name))
            break

    cam.release()

    cv2.destroyAllWindows()

def cropImage(img, top, left, height, width):
    area = (left, top, left+width, top+height)
    cropped_img = img.crop(area)
    return cropped_img

import requests
import io
from dotenv import load_dotenv
load_dotenv()


FACE_KEY = os.getenv("FACE_KEY")
FACE_ENDPOINT = os.getenv("FACE_ENDPOINT")
#print(FACE_KEY, FACE_ENDPOINT)

def detectFace(img):
    # img is a pillow item
    # img = Image.open('memes\\'+filename)
    endpoint = FACE_ENDPOINT
    header = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': str(FACE_KEY)
        }
    output = io.BytesIO()
    img.save(output, format='PNG')
    data = output.getvalue()
    #print(data)
    
    call = requests.post(endpoint, headers=header, data=data)
    #print(call.json())
    return call.json()

def newestSelfie(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)