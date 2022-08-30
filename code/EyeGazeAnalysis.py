import cv2 as cv
import numpy as np
import time
import dlib
import math

detectFace = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("Files/FFD68Pts.dat")

def midpoint(pts1, pts2):
    x, y = pts1
    x1, y1 = pts2
    xOut = int((x + x1)/2)
    yOut = int((y1 + y)/2)
    return (xOut, yOut)

def eucaldainDistance(pts1, pts2):
    x, y = pts1
    x1, y1 = pts2
    eucaldainDist = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return eucaldainDist

def faceDetector(image, gray):
    cordFace1 = (0, 0)
    cordFace2 = (0, 0)
    faces = detectFace(gray)

    face = None
    for face in faces:
        cordFace1 = (face.left(), face.top())
        
        cordFace2 = (face.right(), face.bottom())
    return image, face

def faceLandmakDetector(image, gray, face):
    landmarks = predictor(gray, face)
    pointList = []
    for n in range(0, 68):
        point = (landmarks.part(n).x, landmarks.part(n).y)
        pointList.append(point)
    return image, pointList

def blinkDetector(eyePoints):
    top = eyePoints[1:3]
    bottom = eyePoints[4:6]
    topMid = midpoint(top[0], top[1])
    bottomMid = midpoint(bottom[0], bottom[1])
    VerticalDistance = eucaldainDistance(topMid, bottomMid)
    HorizontalDistance = eucaldainDistance(eyePoints[0], eyePoints[3])
    blinkRatio = (HorizontalDistance/VerticalDistance)
    return blinkRatio, topMid, bottomMid

def EyeTracking(image, gray, eyePoints):
    dim = gray.shape
    mask = np.zeros(dim, dtype=np.uint8)
    PollyPoints = np.array(eyePoints, dtype=np.int32)
    cv.fillPoly(mask, [PollyPoints], 255)
    eyeImage = cv.bitwise_and(gray, gray, mask=mask)
    maxX = (max(eyePoints, key=lambda item: item[0]))[0]
    minX = (min(eyePoints, key=lambda item: item[0]))[0]
    maxY = (max(eyePoints, key=lambda item: item[1]))[1]
    minY = (min(eyePoints, key=lambda item: item[1]))[1]
    eyeImage[mask == 0] = 255
    cropedEye = eyeImage[minY:maxY, minX:maxX]
    height, width = cropedEye.shape
    divPart = int(width/3)
    ret, thresholdEye = cv.threshold(cropedEye, 100, 255, cv.THRESH_BINARY)
    rightPart = thresholdEye[0:height, 0:divPart]
    centerPart = thresholdEye[0:height, divPart:divPart+divPart]
    leftPart = thresholdEye[0:height, divPart+divPart:width]
    rightBlackPx = np.sum(rightPart == 0)
    centerBlackPx = np.sum(centerPart == 0)
    leftBlackPx = np.sum(leftPart == 0)
    pos= Position([rightBlackPx, centerBlackPx, leftBlackPx])
    return mask, pos

def Position(ValuesList):
    maxIndex = ValuesList.index(max(ValuesList))
    posEye = ''
    if maxIndex == 0:
        posEye = "Right"
    elif maxIndex == 1:
        posEye = "Center"
    elif maxIndex == 2:
        posEye = "Left"
    else:
        posEye = "Eye Closed"
    return posEye

def start():

    COUNTER = 0
    TOTAL_BLINKS = 0
    CLOSED_EYES_FRAME = 3
    cameraID = 0
    FRAME_COUNTER = 0
    START_TIME = time.time()
    FPS = 0

    camera = cv.VideoCapture("video.avi")
    right_count = 0
    left_count = 0
    center_count = 0
    no_eyes = 0

    while True:
        FRAME_COUNTER += 1
        # getting frame from camera
        ret, frame = camera.read()
        if ret == False:
            break

        grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        height, width = grayFrame.shape
        circleCenter = (int(width/2), 50)
        # calling the face detector funciton
        image, face = faceDetector(frame, grayFrame)
        if face is not None:
            image, PointList = faceLandmakDetector(frame, grayFrame, face)
            RightEyePoint = PointList[36:42]
            LeftEyePoint = PointList[42:48]
            leftRatio, topMid, bottomMid = blinkDetector(LeftEyePoint)
            rightRatio, rTop, rBottom = blinkDetector(RightEyePoint)
            blinkRatio = (leftRatio + rightRatio)/2
            if blinkRatio > 4:
                COUNTER += 1
            else:
                if COUNTER > CLOSED_EYES_FRAME:
                    TOTAL_BLINKS += 1
                    COUNTER = 0
            mask, pos= EyeTracking(frame, grayFrame, RightEyePoint)
            if pos == 'Right':
                right_count+=1
            elif pos == 'Left':
                left_count+=1
            elif pos == 'Center':
                center_count+=1
        else:
            no_eyes +=1

        SECONDS = time.time() - START_TIME
        FPS = FRAME_COUNTER/SECONDS

    camera.release()
    cv.destroyAllWindows()

    return TOTAL_BLINKS, right_count, left_count, center_count, no_eyes