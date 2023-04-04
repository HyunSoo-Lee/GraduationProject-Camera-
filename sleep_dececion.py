import numpy as np
import dlib 
import cv2  
import math
import time 
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

def detect(gray, frame, sizelist):
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 5, minSize = (100, 100), flags = cv2.CASCADE_SCALE_IMAGE)
    for(x, y, w, h)in faces:
        dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, dlib_rect).parts()])
        #landmarks_display = landmarks[0:68]
        landmarks_display = landmarks[36:48]
        for idx , point in enumerate(landmarks_display):
            pos = (point[0,0], point[0,1])
            cv2.circle(frame, pos, 2, color=(0,255,255), thickness = -1)
        shape = predictor(frame, dlib_rect)
        
        leftR_i_top = (shape.part(38).x, shape.part(38).y)
        leftR_i_bot = (shape.part(40).x, shape.part(40).y)
        leftR_line = cv2.line(frame, leftR_i_top, leftR_i_bot, color=(0,255,255))
        leftR = distance(shape.part(38).x, shape.part(38).y, shape.part(40).x, shape.part(40).y)

        leftL_i_top = (shape.part(37).x, shape.part(37).y)
        leftL_i_bot = (shape.part(41).x, shape.part(41).y)
        leftL_line = cv2.line(frame, leftL_i_top, leftL_i_bot, color=(0,255,255))
        leftL = distance(shape.part(37).x, shape.part(37).y, shape.part(41).x, shape.part(41).y)

        rightR_i_top = (shape.part(44).x, shape.part(44).y)
        rightR_i_bot = (shape.part(46).x, shape.part(46).y)
        rightR_line = cv2.line(frame, rightR_i_top, rightR_i_bot, color=(0,255,255))
        rightR = distance(shape.part(44).x, shape.part(44).y, shape.part(46).x, shape.part(46).y)

        rightL_i_top = (shape.part(43).x, shape.part(43).y)
        rightL_i_bot = (shape.part(47).x, shape.part(47).y)
        rightL_line = cv2.line(frame, rightL_i_top, rightL_i_bot, color=(0,255,255))
        rightL = distance(shape.part(43).x, shape.part(43).y, shape.part(47).x, shape.part(47).y)

        left = (leftR + leftL)/2
        right = (rightR + rightL)/2
        print("left eye size is {} \nright eye size is {}\n\n".format(left, right))

        eye_avg = (left + right) / 2
        while len(sizelist) != 500:
            sizelist.append(eye_avg)
            break
        sorted_size = sorted(sizelist)
        max_values = sorted_size[-50:]
        average = sum(max_values) / len(max_values)

        cv2.putText(frame, str(average), (10, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 2)


    return frame

video_capture = cv2.VideoCapture(0)
sizelist = []

while True:
    _,frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canvas = detect(gray,frame,sizelist)

    cv2.imshow("test", canvas)
    print(sizelist)
    time.sleep(0.25)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()