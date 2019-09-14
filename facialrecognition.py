#https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/python-sdk
import asyncio, io, glob, os, sys, time, uuid, requests, random
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

from dotenv import load_dotenv
load_dotenv()

key = os.environ["FACE_KEY"]
endpoint = os.environ["FACE_ENDPOINT"]

meme_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/Memes"
meme_path = ""
for r, d, f in os.walk(meme_folder_path):
    randomint = random.randint(1,len(f))
    meme_path = meme_folder_path + f[randomint]
    print (meme_path)
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


# # Convert width height to a point in a rectangle
# def getRectangle(faceDictionary):
#     rect = faceDictionary['face_rectangle']
#     left = rect['left']
#     top = rect['top']
#     bottom = left + rect['height']
#     right = top + rect['width']
#     return ((left, top), (bottom, right))

# # Download the image from the url
# response = requests.get(single_face_image_url)
# img = Image.open(BytesIO(response.content))

# # For each face returned use the face rectangle and draw a red box.
# draw = ImageDraw.Draw(img)
# for face in detected_faces:
#     draw.rectangle(getRectangle(face), outline='red')

# # Display the image in the users default image browser.
# img.show()

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}