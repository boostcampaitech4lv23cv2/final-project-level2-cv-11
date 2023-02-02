import os
import sys
import requests

from dotenv import load_dotenv


class Font_Color:
    def find_color(self, merged_boxes):
        from scipy import stats
        import numpy as np
        np.set_printoptions(threshold=sys.maxsize)
        
        color_code = []
        for boxes in merged_boxes:
            for i in range(len(boxes[3])):
                if len(boxes[3][i][3]) != 0:
                    box = boxes[3][i][3][0]
                    box = np.transpose(box,(2,0,1))
                    
                    b = box[0].flatten()
                    g = box[1].flatten()
                    r = box[2].flatten()
                    
                    condition  = np.where(np.sum((r,g,b),axis = 0)> 740)
                    b = np.delete(b,condition)
                    g = np.delete(g,condition)
                    r = np.delete(r,condition)
                    
                    b = stats.mode(b, keepdims = True)[0].item()
                    g = stats.mode(g, keepdims = True)[0].item()
                    r = stats.mode(r, keepdims = True)[0].item()
                    break
            color_code.append(f'#{r:02X}{g:02X}{b:02X}')
        return color_code
            
            
    