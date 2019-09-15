#https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/python-sdk
import asyncio, io, glob, os, sys, time, uuid, requests, random, cv2
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

from dotenv import load_dotenv
load_dotenv()

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





key = os.environ["FACE_KEY"]
endpoint = os.environ["FACE_ENDPOINT"]
user_top = 0
user_left = 0
user_height = 100
user_width = 100


meme_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/Memes"
meme_path = ""

user_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/UserPhotos"

take_photo()


for r, d, f in os.walk(meme_folder_path):
    randomint = random.randint(1,len(f))
    meme_path = meme_folder_path + "/" + f[randomint]
    print (meme_path)
    cropImage(meme_path, user_top, user_left, user_height, user_width).show()
    #f is the list of files in list


face_client = FaceClient(endpoint, CognitiveServicesCredentials(key))

# Detect a face in an image that contains a single face
single_face_image_url = "https://scontent.fyyz1-1.fna.fbcdn.net/v/t1.15752-9/70888134_2522150378019046_2182028800106168320_n.png?_nc_cat=111&_nc_oc=AQl7S4cmsiXW0dJpeqZDfE6ZAe0azVJ0q3ULjB7iN2zoZx3p4vq_RpO-dHD1-okLlvw&_nc_ht=scontent.fyyz1-1.fna&oh=64c57e1b621411f92ea903ae527d62c9&oe=5DF2D71A"
single_image_name = os.path.basename(single_face_image_url)

detected_faces = face_client.face.detect_with_url(url=single_face_image_url)
if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))
else:
    print(detected_faces[0].face_rectangle)
    print('face detected')

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}