import pytesseract
import cv2 
import matplotlib.pyplot as plt
from PIL import Image
import os

class Tesseract_OCR:
    
    def ocr(self, merged_boxes, img):
        
        for m in merged_boxes:
            x1 = m[0][0]
            x2 = m[1][0]
            y1 = m[0][1]
            y2 = m[1][1]
            img_crop = img[y1 : y2+1, x1 : x2+1]
            boxes = pytesseract.image_to_boxes(img_crop, lang='kor')
            
            img_crop_letters = []
            for b in boxes.splitlines():
                b = b.split(' ')
                cx1,cy1,cx2,cy2 = int(b[1]),int(b[2]),int(b[3]),int(b[4])
                h = y2 - y1
                img_crop_letters.append(img_crop[h-cy2:h-cy1+1,cx1:cx2])
            
            m.append(img_crop_letters)
        
        return merged_boxes
        
        
        