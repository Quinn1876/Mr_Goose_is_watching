#https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/python-sdk
import asyncio, io, glob, os, sys, time, uuid, requests
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

print()
print(endpoint)
print()

face_client = FaceClient(endpoint, CognitiveServicesCredentials(key))

# Detect a face in an image that contains a single face
single_face_image_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
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