import cv2


class typical_pipeline():
    
    def __init__(self):
        self.OCR = Clova_OCR()
        self.re_OCR = Tesseract_OCR()
        self.MT = Papago_MT()
        self.Classification = Typical_FC()
    
    def go(self, image_path):
        img = cv2.imread(image_path)
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        merged_boxes = self.OCR.ocr(image_path)
        merged_boxes_with_crop = self.re_OCR.ocr(merged_boxes, self.img)
        classified_boxes = self.Classification.classification(merged_boxes_with_crop)
        result = self.MT.machine_translate(classified_boxes)
        
        print(result)

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        print(path.dirname( path.dirname( path.abspath(__file__) ) ))
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
        from model.OCR.clova_OCR import Clova_OCR
        from model.OCR.tesseract_OCR import Tesseract_OCR
        from MachineTranslate.papago_MT import Papago_MT
        from font_classifier.typical_FC import Typical_FC
    
    a = typical_pipeline()
    a.go('/opt/level3_productserving-level3-cv-11/notebooks/image/imsi2.PNG')