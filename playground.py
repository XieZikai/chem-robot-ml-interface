import requests
import json
import base64
import sqlite3
import datetime

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

s = encode_image_to_base64(r'D:\3.png')
time = str(datetime.datetime.now())
image = s
prediction = 2

from apps.robot_control.cv_model import load_model, test_model_on_base64_image

model = load_model(r'C:\Users\darkn\PycharmProjects\flask-atlantis-dark-master\apps\robot_control\solubility_model.pth')
device = 'cpu'
img = image

print(test_model_on_base64_image(model, image, device))
