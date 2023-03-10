import cv2
import pandas as pd
import numpy as np
import av


faceProto = 'static/opencv_face_detector.pbtxt'
faceModel = 'static/opencv_face_detector_uint8.pb'

ageProto = 'static/age_deploy.prototxt'
ageModel = 'static/age_net.caffemodel'

genderProto = 'static/gender_deploy.prototxt'
genderModel = 'static/gender_net.caffemodel'

faceNet = cv2.dnn.readNet(faceModel,faceProto)
ageNet = cv2.dnn.readNet(ageModel,ageProto)
genderNet = cv2.dnn.readNet(genderModel,genderProto)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

def faceBox(faceNet,frame):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame,1.0,(227,227), [104,127,123])
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bbox = []
    for i in range(detection.shape[2]):
        confidence = detection[0,0,i,2]
        if confidence > 0.7:
            x1 = int(detection[0,0,i,3]*frameWidth)
            y1 = int(detection[0,0,i,4]*frameHeight)
            x2 = int(detection[0,0,i,5]*frameWidth)
            y2 = int(detection[0,0,i,6]*frameHeight)
            bbox.append([x1,y1,x2,y2])
            cv2.rectangle(frame,(x1,y1),(x2,y2), (0,255,0), 1)
    return frame,bbox

class VideoProcessor:
    def recv(self,frames):
        frame = frames.to_ndarray(format='bgr24')
        frame,bboxs = faceBox(faceNet,frame)
        for bbox in bboxs:
            face = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            blob = cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES)
            genderNet.setInput(blob)
            genderPred = genderNet.forward()
            gender = genderList[genderPred[0].argmax()]

            ageNet.setInput(blob)
            agePred = ageNet.forward()
            age = ageList[agePred[0].argmax()]

            label ="{},{}".format(gender,age)
            cv2.rectangle(frame,(bbox[0],bbox[1]-10), (bbox[2], bbox[1]), (255,255,255), 1)
            cv2.putText(frame,label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,(255,255,255), 2,cv2.LINE_AA)

            return av.VideoFrame.from_ndarray(frame, format='bgr24')