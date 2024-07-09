from ultralytics import YOLO
import cv2
model = YOLO(r"C:\Users\hp\Downloads\best.pt")

def processPredict(image):
    img=cv2.resize(image,(640,640))
    pred=model.predict(img)
    names=model.names
    text=""
    dp={"normal":[],"benign":[],"malignant":[]}
    name=[]
    for r in pred:
        for c in r.boxes.cls:
            name.append(names[int(c)])
    for i in range(len(name)):
        dp[name[i]].append(pred[0].boxes.xyxy[i])
    
    if len(dp['malignant'])!=0:
        text="last stage of lung cancer"
        return text,dp['malignant']
    elif len(dp['benign'])!=0:
        text="initial stage of lung cancer"
        return text,dp['benign']
    else:
        text="normal nothing to worry"
        return text,dp['normal']







