import argparse
import base64
import json
import cv2

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import time
from PIL import Image
from PIL import ImageOps
from flask import Flask, render_template
from io import BytesIO

from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array


sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None

@sio.on('telemetry')
def telemetry(sid, data):
    # The current steering angle of the car
    steering_angle = data["steering_angle"]
    # The current throttle of the car
    throttle = data["throttle"]
    # The current speed of the car
    speed = data["speed"]
    # The current image from the center camera of the car
    imgString = data["image"]
    image = Image.open(BytesIO(base64.b64decode(imgString)))
    image_array = np.asarray(image)
    # BGR to RGB
    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    # image adjust
    process_image = image_array[80:140, 0:320]
    process_image = cv2.resize(process_image, (128, 128)) / 255. - 0.5
    
    # image 3 dimension to 1 dimension
    transformed_image_array = process_image[None, :, :, :]
    # This model currently assumes that the features of the model are just the images. Feel free to change this.
    steering_angle = float(model.predict(transformed_image_array, batch_size=1))
    # The driving model currently just outputs a constant throttle. Feel free to edit this.
    if float(speed) < 20:
        throttle = 0.5
    else:
        throttle = 0.2
    print(steering_angle, throttle, speed)
    send_control(steering_angle, throttle)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit("steer", data={
             'steering_angle': steering_angle.__str__(),
             'throttle': throttle.__str__()
             }, skip_sid=True)


if __name__ == '__main__':
    model = load_model('model.h5')
    
    # Bind the flash application to the middleware
    app = socketio.Middleware(sio, app)
    
    # Start eventlet, wgsi server, and listen to port 4567.
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
