import pytesseract
import cv2 
from PIL import Image
import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

class Tesseract_OCR:

    
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
        
        
        