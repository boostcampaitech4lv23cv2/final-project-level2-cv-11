import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
import model
import numpy as np
import cv2

class typical_pipeline():
    
    def __init__(self):
        self.OCR = model.Clova_OCR()
        self.re_OCR = model.Tesseract_OCR()
        self.MT = model.Papago_MT()
        self.Classification = model.Typical_FC("typical_font")
    
    def go(self, image):
        encoded_img = np.fromstring(image, dtype = np.uint8)
        self.img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        #self.img = cv2.imread(image)
        #self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        merged_boxes = self.OCR.ocr(image)
        merged_boxes_with_crop = self.re_OCR.ocr(merged_boxes, self.img)
        classified_boxes = self.Classification.classification(merged_boxes_with_crop)
        result = self.MT.machine_translate(classified_boxes)
        
        # import pprint
        # pp = pprint.PrettyPrinter()
        # pp.pprint(result)
        return result
    
import pickle
with open("/opt/level3_productserving-level3-cv-11/Gobuk.pickle","rb") as fr:
    data = pickle.load(fr)
a = typical_pipeline()
print(a.go(data))

    