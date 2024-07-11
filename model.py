from ultralytics import YOLO
import io
from PIL import Image,ImageDraw
model = YOLO(r"C:\Users\hp\Downloads\best.pt")

def processPredict(image):
    img=Image.open(image)
    img=img.resize((640,640))
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
        text="normal condition nothing to worry"
        return text,dp['normal']

def drawRectangle(rectangle,image):
    img=Image.open(image)
    draw=ImageDraw.Draw(img)
    for i in rectangle:
        draw.rectangle(((i[0],i[1]),(i[2],i[3])),outline="red")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr










