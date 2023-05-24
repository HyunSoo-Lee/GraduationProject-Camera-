import numpy as np
import dlib 
import cv2  
import math
import time 
import current_time as curtime
import db_connect as db
predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat') 
#faceCascade = cv2.CascadeClassifier('/home/pi/opencv/opencv-4.6.0/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
MOUTH = list(range(48, 68))
NOSE = list(range(27, 36))
EYEBROWS = list(range(17, 27))
JAWLINE = list(range(1, 17))
ALL = list(range(0, 68))
EYES = list(range(36, 48))

def distance(ax, ay, bx, by):
    x = ax - bx
    y = ay - by
    c = math.sqrt((x*x) + (y*y))
    return c

def detect(gray, frame, val, t):
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 5, minSize = (100, 100), flags = cv2.CASCADE_SCALE_IMAGE)
    for(x, y, w, h)in faces:
        dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, dlib_rect).parts()])
        #landmarks_display = landmarks[0:68]
        landmarks_display = landmarks[36:48]
        for idx , point in enumerate(landmarks_display):
            pos = (point[0,0], point[0,1])
            #cv2.circle(frame, pos, 2, color=(0,255,255), thickness = -1)
        shape = predictor(frame, dlib_rect)
        
        leftR_top = (shape.part(38).x, shape.part(38).y)
        leftR_bot = (shape.part(40).x, shape.part(40).y)
        #cv2.line(frame, leftR_top, leftR_bot, color=(0,255,255))
        leftR = distance(shape.part(38).x, shape.part(38).y, shape.part(40).x, shape.part(40).y)

        leftL_top = (shape.part(37).x, shape.part(37).y)
        leftL_bot = (shape.part(41).x, shape.part(41).y)
        #cv2.line(frame, leftL_top, leftL_bot, color=(0,255,255))
        leftL = distance(shape.part(37).x, shape.part(37).y, shape.part(41).x, shape.part(41).y)

        leftC_top = (shape.part(36).x, shape.part(36).y)
        leftC_bot = (shape.part(39).x, shape.part(39).y)
        #cv2.line(frame, leftC_top, leftC_bot, color=(0,255,255))
        leftC = distance(shape.part(36).x, shape.part(36).y, shape.part(39).x, shape.part(39).y)

        EAR_left = (leftR + leftL)/(2.0 * leftC)

        rightR_top = (shape.part(44).x, shape.part(44).y)
        rightR_bot = (shape.part(46).x, shape.part(46).y)
        #cv2.line(frame, rightR_top, rightR_bot, color=(0,255,255))
        rightR = distance(shape.part(44).x, shape.part(44).y, shape.part(46).x, shape.part(46).y)

        rightL_top = (shape.part(43).x, shape.part(43).y)
        rightL_bot = (shape.part(47).x, shape.part(47).y)
        #cv2.line(frame, rightL_top, rightL_bot, color=(0,255,255))
        rightL = distance(shape.part(43).x, shape.part(43).y, shape.part(47).x, shape.part(47).y)

        rightC_top = (shape.part(42).x, shape.part(42).y)
        rightC_bot = (shape.part(45).x, shape.part(45).y)
        #cv2.line(frame, rightC_top, rightC_bot, color=(0,255,255))
        rightC = distance(shape.part(42).x, shape.part(42).y, shape.part(45).x, shape.part(45).y)

        EAR_right = (rightR + rightL)/(2.0 * rightC)
        EAR = round((EAR_right + EAR_left) / 2.0, 2)
        cv2.putText(frame, str(EAR), (10, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (221, 160, 221))

        #print(EAR)
        if EAR <= 0.2:
            if val == False:
                val = not val
                t = time.time()
            else:
                continue
        else:
            if val == True:
                val = not val
                t = time.time()
            continue
    return frame, val, t

video_capture = cv2.VideoCapture(0)

val = False
t = 0
startt = 0
endt = 0
time_arr = [0,0]
while True:
    if time_arr[0] != 0 and time_arr[1] != 0:
        sleep_time = time_arr[1] - time_arr[0]
        sleep_time = int(sleep_time)
        print(sleep_time , '동안 눈을 감고 있었습니다.')
        db.edit_val(1, 'sleep_time', 'startt', startt)
        db.edit_val(1, 'sleep_time', 'endt', endt)
        time_arr = [0,0]
    _,frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    arr = detect(gray,frame, val, t)
    canvas = arr[0]
    val = arr[1]
    cv2.imshow("test", canvas)
    #print(sizelist)
    time.sleep(0.25)
    if arr[2] != 0 and val == True:
        #print('Blink!', arr[2])
        time_arr[0] = arr[2]
        startt = curtime.get_time()
    if arr[2] != 0 and val == False:
        #print('Blink!', arr[2])
        time_arr[1] = arr[2]
        endt = curtime.get_time()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()