import os
import json
from PIL import Image,ImageDraw,ImageFont

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def create_font(font_list, font_name, text_width, text_height, save_path, text, idx):
    
    for font, name in zip(font_list, font_name):
        # 이미지 객체 생성 (배경 검정)
        canvas = Image.new('RGB', (text_width, text_height), "white")
        
        # 가운데에 그리기 (폰트 색: 하양)
        draw = ImageDraw.Draw(canvas)
        w, h = font.getsize(text)
        draw.text(((text_width-w)/2.0,(text_height-h)/2.0), text, 'black', font)
        
        directory = os.path.join(save_path ,name.split(".")[0])
        createDirectory(directory)
        
        # png로 저장 및 출력해서 보기
        if idx == None:
            canvas.save(os.path.join(directory, name.split(".")[0] + "_"+ text + '.png'), "PNG")
        else:
            canvas.save(os.path.join(directory, name.split(".")[0] + "_others_" + str(idx)+'.png'), "PNG")
        canvas.show()


## 폰트 파일 위치
font_path = '/opt/level3_productserving-level3-cv-11/data/fonts'
font_name = os.listdir(font_path)

## 한글 json 위치
json_path = '/opt/level3_productserving-level3-cv-11/data/words/ko/ko.json'


with open(json_path, 'r', encoding='utf-8') as f:
    json_file = json.load(f)
    
lang = json_file['words']['lang']

save_path = os.path.join("/opt/level3_productserving-level3-cv-11/data/words", lang, 'images')

# 폰트 생성 옵션(ex. 폰트 크기)
font_list = [ImageFont.truetype(os.path.join(font_path, name), 100) for name in font_name]

# 이미지 사이즈 지정
text_width = 256
text_height = 256

for type in json_file.keys():
    for idx, text in enumerate(json_file[type]['character']):
        if type == 'words':
            create_font(font_list, font_name, text_width, text_height, save_path, text, None)
        else:
            create_font(font_list, font_name, text_width, text_height, save_path, text, idx)