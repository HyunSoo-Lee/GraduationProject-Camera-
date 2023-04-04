import numpy as np
import dlib 
import cv2  
import math
import time
from pathlib import Path

#  ****eye detection file path****
predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat') 
#faceCascade = cv2.CascadeClassifier('/home/pi/opencv/opencv-4.6.0/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#  ****lying pose dectection file path****
BASE_DIR=Path(__file__).resolve().parent
protoFile = "C:/Users/ocean/Desktop/dev/python/opse/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "C:/Users/ocean/Desktop/dev/python/opse/pose_iter_160000.caffemodel"
 

# body setting
BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]

# eye setting
RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
MOUTH = list(range(48, 68))
NOSE = list(range(27, 36))
EYEBROWS = list(range(17, 27))
JAWLINE = list(range(1, 17))
ALL = list(range(0, 68))
EYES = list(range(36, 48))

inputWidth=320;
inputHeight=240;
inputScale=1.0/255;

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
        landmarks_display = landmarks[36:48]
        for idx , point in enumerate(landmarks_display):
            pos = (point[0,0], point[0,1])
            cv2.circle(frame, pos, 2, color=(0,255,255), thickness = -1)
        shape = predictor(frame, dlib_rect)
        
        leftR = distance(shape.part(38).x, shape.part(38).y, shape.part(40).x, shape.part(40).y)
        leftL = distance(shape.part(37).x, shape.part(37).y, shape.part(41).x, shape.part(41).y)
        rightR = distance(shape.part(44).x, shape.part(44).y, shape.part(46).x, shape.part(46).y)
        rightL = distance(shape.part(43).x, shape.part(43).y, shape.part(47).x, shape.part(47).y)

        left = (leftR + leftL)/2
        right = (rightR + rightL)/2
        print("left eye size is {} \nright eye size is {}\n\n".format(left, right))

        eye_avg = (left + right) / 2
        print(eye_avg)
        while len(sizelist) != 500:
            sizelist.append(eye_avg)
            break
        sorted_size = sorted(sizelist)
        max_values = sorted_size[-50:]
        average = sum(max_values) / len(max_values)

        cv2.putText(frame, str(average), (10, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 2)

def lying_detection(image, pt1, pt2, pt3):
    # 모든 점이 존재하는 경우에만 라인을 그립니다.
    if pt1 is not None and pt2 is not None and pt3 is not None:
        text1 = "Lying Left"
        text2 = "Lying Right"
        text3 = "Lying prone"
        begin_right = 0
        begin_left = 0
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)
        cv2.line(image, pt2, pt3, (0, 255, 0), 2)
        print("chest is ", pt2)
        print("arm1 is ", pt1)
        print("arm2 is ", pt3)
        if pt1[0] > pt2[0] and pt3[0] > pt2[0]:
            #cv2.putText(image, text1, (10, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 2)
            print(text1)
            begin_left = time.time()
        end_left = time.time()
        print("lying left time" + str(end_left - begin_left))
        if begin_left != 0:
            result_left =  round(end_left - begin_left),2
            #if result_left >= 60:
                #응애 자고있음 -> 쿼리문 날려야함
        if pt1[0] < pt2[0] and pt3[0] < pt2[0]:
            #cv2.putText(image, text2, (10, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 2)
            print(text2)
            begin_right = time.time()
        end_right = time.time()
        print("lying right time" + str(end_right - begin_right))
        if begin_right != 0:
            result_right = round(end_right - begin_right),2
            #if result_left >= 60:
                #응애 자고있음 -> 쿼리문 날려야함
        # if pt1[0] > pt3[0]:
        #     cv2.putText(image, text3, (10, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 2)

sizelist = []
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
capture = cv2.VideoCapture(0)

while cv2.waitKey(1) < 0:
    hasFrame, frame = capture.read()
    #웹캠 오류시 중지
    if not hasFrame:
        cv2.waitKey()
        break
    
    # basic info & converting to gray scale
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    # eye detect
    canvas = detect(gray,frame,sizelist)
    #print(sizelist)

    # motion detect
    inpBlob = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False, crop=False)
    imgb=cv2.dnn.imagesFromBlob(inpBlob)
    net.setInput(inpBlob)
    output = net.forward()
    points = []
    for i in range(0,15):
        # 해당 신체부위 신뢰도 얻음.
        probMap = output[0, i, :, :]
        # global 최대값 찾기
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        # 원래 이미지에 맞게 점 위치 변경
        x = (frameWidth * point[0]) / output.shape[3]
        y = (frameHeight * point[1]) / output.shape[2]
        # 키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로    
        if prob > 0.1 :    
            #cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED) # circle(그릴곳, 원의 중심, 반지름, 색)
            #cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
            points.append((int(x), int(y)))
        else :
            points.append(None)

    lying_detection(frame, points[3], points[14], points[6])

    cv2.imshow("result", frame)

capture.release()  #카메라 장치에서 받아온 메모리 해제
cv2.destroyAllWindows() #모든 윈도우 창 닫음