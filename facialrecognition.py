#https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/python-sdk
import asyncio, io, glob, os, sys, time, uuid, requests, random, cv2
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from Img_handler import resizeImg, imgComposition, cropImage, take_photo, detectFace, newestSelfie

from dotenv import load_dotenv
load_dotenv()

key = os.environ["FACE_KEY"]
endpoint = os.environ["FACE_ENDPOINT"]
user_top = 0
user_left = 0
user_height = 100
user_width = 100

meme_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/Memes"
user_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/UserPhotos"
final_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/FinalProduct"


meme_path = ""
path, dirs, files = next(os.walk(user_folder_path))
take_photo(len(files))
user_path = newestSelfie(user_folder_path)
#setup the user_photo

r, d, f = next (os.walk(meme_folder_path))
randomint = random.randint(1,len(f))
meme_path = meme_folder_path + "/" + f[randomint-1]
#setup the meme photo


user_pillow = Image.open(user_path)
meme_pillow = Image.open(meme_path)

user_json = detectFace(user_pillow)
meme_json = detectFace(meme_pillow)

print(user_json)


cropped_user_pillow = cropImage(user_pillow, **user_json[0]["faceRectangle"])

resized_cropped_user_pillow = resizeImg(cropped_user_pillow, (user_json[0]["faceRectangle"]["width"],user_json[0]["faceRectangle"]["height"]))#width,height

final_product = imgComposition(meme_pillow, resized_cropped_user_pillow, meme_json[0]["faceRectangle"]["top"], meme_json[0]["faceRectangle"]["left"])

r, d, f = next (os.walk(final_folder_path))
print(final_folder_path + "final_product_{}.bmp".format(len(f) + 1))
final_product.save(final_folder_path + "/final_product_{}.bmp".format(len(f) + 1), 'bmp')
final_product.show()