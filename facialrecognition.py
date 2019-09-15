#https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/python-sdk
import asyncio, io, glob, os, sys, time, uuid, requests, random, cv2, base64
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
buffered = BytesIO()
user_pillow.save(buffered, format="JPEG")
user_pillow_string = base64.b64encode(buffered.getvalue())



response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(user_path, 'rb')},
    data={'size': 'auto'},  
    headers={'X-Api-Key': 'fQtRqoeiDP9VEKSkP6jQhTtb'},
)
if response.status_code == requests.codes.ok:
    buffered = io.BytesIO()
    buffered.write(response.content)
    buffered.seek(0)
    user_background_gone = Image.open(buffered)
else:
    print("Error:", response.status_code, response.text)



meme_pillow = Image.open(meme_path)

user_json = detectFace(user_pillow)
meme_json = detectFace(meme_pillow)

print(user_json)


cropped_user_pillow = cropImage(user_background_gone, **user_json[0]["faceRectangle"])
#cropped_meme_pillow = cropImage(meme_pillow, **meme_json[0]["faceRectangle"])


resized_cropped_user_pillow = resizeImg(cropped_user_pillow, (meme_json[0]["faceRectangle"]["width"],meme_json[0]["faceRectangle"]["height"]))#width,height

#squareFace = Image.blend(resized_cropped_user_pillow, cropped_meme_pillow, 0.2)


#resized_cropped_user_pillow = Image.convert(mode=cropped_meme_pillow.mode)
#squareFace = Image.composite(cropped_meme_pillow, resized_cropped_user_pillow, "RGBA")
#________________________________#




final_product = imgComposition(meme_pillow, resized_cropped_user_pillow, meme_json[0]["faceRectangle"]["top"], meme_json[0]["faceRectangle"]["left"])

r, d, f = next (os.walk(final_folder_path))
print(final_folder_path + "final_product_{}.bmp".format(len(f) + 1))
final_product.save(final_folder_path + "/final_product_{}.bmp".format(len(f) + 1), 'bmp')
final_product.show()