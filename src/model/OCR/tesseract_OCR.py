import pytesseract
import cv2 
from PIL import Image
import os
import numpy as np

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

class Tesseract_OCR:
    
    def __init__(self, class_type):
        self.type = class_type

    
    def untypical_ocr(self, merged_boxes, img):
        
        for idx, m in enumerate(merged_boxes):
            x1 = m[0][0]
            x2 = m[1][0]
            y1 = m[0][1]
            y2 = m[1][1]
            img_crop = img[y1 : y2+1, x1 : x2+1]
            boxes = pytesseract.image_to_boxes(img_crop, lang='kor')
            img_crop_letters = []
            for idx2, b in enumerate(boxes.splitlines()):
                b = b.split(' ')
                cx1,cy1,cx2,cy2 = int(b[1]),int(b[2]),int(b[3]),int(b[4])
                h = y2 - y1
                cropped_image = img_crop[h-cy2:h-cy1+1,cx1:cx2+1]
                
                if len(cropped_image) == 1:
                    continue
        
                createDirectory(os.path.join(os.getenv('HOME'),f'tmp/img{idx}/referenced'))
                cv2.imwrite(os.path.join(os.getenv('HOME'),f'tmp/img{idx}/referenced/{idx2}.png'),cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY))
                i,j,k = cropped_image.shape
                if i and j  and k :
                    img_crop_letters.append(cropped_image)
            
            m.append(img_crop_letters)
        
        return merged_boxes
    
    def typical_ocr(self, merged_boxes, img):
        
        h, w, _ = img.shape
        
        for m in merged_boxes:
            x1 = m[0][0]
            x2 = m[1][0]
            y1 = m[0][1]
            y2 = m[1][1]
            img_crop = img[y1 : y2+1, x1 : x2+1]
            boxes = pytesseract.image_to_boxes(img_crop, lang='kor')
            
            # if len(boxes) != 0:
            #     for b in boxes.splitlines():
            #         b = b.split(' ')
            #         img = cv2.rectangle(img, (x1+int(b[1]), y2-int(b[2])), (x1+int(b[3]), y2-int(b[4])), (0, 255, 0), 2)       
            
            img_crop_letters = []
            for b in boxes.splitlines():
                b = b.split(' ')
                cx1,cy1,cx2,cy2 = int(b[1]),int(b[2]),int(b[3]),int(b[4])
                h = y2 - y1
                cropped_image = img_crop[h-cy2:h-cy1+1,cx1:cx2]
                i,j,k = cropped_image.shape
                if i and j  and k :
                    img_crop_letters.append(cropped_image)
            
            m.append(img_crop_letters)
        
        
        return merged_boxes
    
    def n_divide(self, merged_boxes, img):
  
        for idx, m in enumerate(merged_boxes):
            tmp_num = 0
            for little_box in m[3]:
                x1 = little_box[0][0]
                x2 = little_box[1][0]
                y1 = little_box[0][1]
                y2 = little_box[1][1]
                txt = list(little_box[2])
                
                char_width = np.array([0.])
                char_true = []
                for order, tx in enumerate(txt):
                    flag = 0
                    if order == len(txt) -1 or order == 0:
                        flag = 1.5
                        
                    if tx.isalpha():
                        char_width = np.append(char_width,10 + flag)
                        char_true.append(True)
                    elif tx in "?~^":
                        char_width = np.append(char_width,6 + flag)
                        char_true.append(False)
                    elif tx in "!., ":
                        char_width = np.append(char_width,3.3 + flag)
                        char_true.append(False)
                        
                char_width *= (x2-x1) / np.sum(char_width)
                char_width = np.round(char_width, 0)
                char_width = np.cumsum(char_width)
                char_width = char_width.tolist()
                
                
                img_crop_letters = []
                for i in range(len(char_width)-1):
                    if char_true[i]:
                        img_crop_letter = img[y1 : y2+1, x1 + int(char_width[i]) : x1 + int(char_width[i+1])]
                        img_crop_letters.append(img_crop_letter)
                        if self.type == "untypical":
                            createDirectory(os.path.join(os.getenv('HOME'),f'tmp/img{idx}/referenced'))
                            cv2.imwrite(os.path.join(os.getenv('HOME'),f'tmp/img{idx}/referenced/{tmp_num}.png'),cv2.cvtColor(img_crop_letter, cv2.COLOR_BGR2GRAY))
                            tmp_num += 1
                little_box.append(img_crop_letters)
                
        return merged_boxes
        
        
        