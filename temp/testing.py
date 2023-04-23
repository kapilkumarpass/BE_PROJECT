import numpy as np
import cv2
from keras.models import load_model
from tensorflow.keras.models import model_from_json
# from model import FacialExpressionModel



haarcascade = "haarcascade_frontalface_default.xml"
font = cv2.FONT_HERSHEY_PLAIN
emotion_arr = ['Anger','Happy','Neutral','Sad']
print("+" * 50, "loading model")
json_file = open('emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("emotion_model.h5")
cascade = cv2.CascadeClassifier(haarcascade)

found = False
cap = cv2.VideoCapture(0)
while not (0):
    _, frm = cap.read()

    gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in faces:

        fc = gray[y:y + h, x:x + w]
        roi = cv2.resize(fc, (48, 48))
        pred = loaded_model.predict(roi[np.newaxis, :, :, np.newaxis])
        # print(pred)
        # print(np.argmax(pred))
        emotion = emotion_arr[np.argmax(pred)]
        print(emotion)
        cv2.putText(frm, emotion, (x + (w // 3), y - 5), font, 3, (0, 0, 255), 2)

        cv2.rectangle(frm, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("cam", frm)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()



