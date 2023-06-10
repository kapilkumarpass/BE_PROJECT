from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import numpy as np
import cv2
from keras.models import load_model
from tensorflow.keras.models import model_from_json
import time
from django.db import connections
import cv2
import json
import threading

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        haarcascade = "C:\\Users\\kapil\\OneDrive\\Desktop\\be_project\\backend\\temp\\haarcascade_frontalface_default.xml"
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.emotion_arr = ['Angry','Happy','Neutral','Sad']
        # self.emotion_arr = ['Angry','Angry','Angry','Angry']
        print("+" * 50, "loading model")
        json_file = open('C:\\Users\\kapil\\OneDrive\\Desktop\\be_project\\backend\\temp\\emotion_model.json', "r")
        loaded_model_json = json_file.read()
        json_file.close()
        self.emotionlist = []
        self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights("C:\\Users\\kapil\\OneDrive\\Desktop\\be_project\\backend\\temp\\emotion_model.h5")
        self.cascade = cv2.CascadeClassifier(haarcascade)
        (self.grabbed, self.frame) = self.video.read()
        self.t1 = threading.Thread(target=self.update, args=())
        self.t1.start()
      
    def __del__(self):
        self.video.release()

    def get_frame(self):
        frm = self.frame
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:

            fc = gray[y:y + h, x:x + w]
            roi = cv2.resize(fc, (48, 48))
            pred = self.loaded_model.predict(roi[np.newaxis, :, :, np.newaxis])
            emotion = self.emotion_arr[np.argmax(pred)]
            print(emotion)
            self.emotionlist.append(emotion)
            cv2.putText(frm, emotion, (x + (w // 3), y - 5), self.font, 3, (0, 0, 255), 2)

            cv2.rectangle(frm, (x, y), (x + w, y + h), (255, 0, 0), 2)
        _, jpeg = cv2.imencode('.jpg', frm)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if not self.grabbed:
                break

def gen(camera):
     while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')