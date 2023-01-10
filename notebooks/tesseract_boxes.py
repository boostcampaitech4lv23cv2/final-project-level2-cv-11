import pytesseract
import cv2 
import matplotlib.pyplot as plt
from PIL import Image
import os

paths = ['/opt/ml/final_project/imsi/test_2.png',
         '/opt/ml/final_project/imsi/test_3.png',
         '/opt/ml/final_project/imsi/test_4.png',
         '/opt/ml/final_project/imsi/test_5.png',
         '/opt/ml/final_project/imsi/test_6.png']  # 인풋 이미지 경로
result_root = '/opt/ml/level3_productserving-level3-cv-11/notebooks/tesseract_boxes_results/'  # box 그려진 이미지 저장 경로

for path in paths: 
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # use Tesseract to OCR the image 
    name = path.split('/')[-1]
    print(name)
    hImg,wImg,_ = img.shape
    boxes = pytesseract.image_to_boxes(img, lang='kor')
    for b in boxes.splitlines(): 
        b = b.split(' ')
        x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
        cv2.rectangle(img,(x,hImg-y),(w,hImg-h),(0,0,255),1)
        cv2.putText(img,b[0],(x,hImg-y+20),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    text = pytesseract.image_to_string(img, lang='kor')
    if not os.path.exists(result_root): 
        os.mkdir(result_root)
    cv2.imwrite(os.path.join(result_root, name), img)
    print(text)