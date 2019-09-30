# Using Google Vision API
# -*- coding: utf-8 -*-
import io
from google.cloud import vision
import os


class text():

    def recognize(image_path, json_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
        client = vision.ImageAnnotatorClient()

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        idl = []
        for text in texts:
            idl.append(text.description)

        return(idl[0])
        #print('recognize works')
        #return '1234'

'''
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/gangwei/Desktop/smartparker/textdetect-52e8d68b62cc.json"
client = vision.ImageAnnotatorClient()

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
#for text in texts:
print(texts[1].description)'''