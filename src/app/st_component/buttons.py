import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import io
from io import BytesIO
import numpy as np
import os


## 폰트 파일 위치
font_path = '/opt/ml/Final_Project/level3_productserving-level3-cv-11/data/fonts/typical'


def btn_generation():
    bcol1, bcol2, bcol3 , bcol4, bcol5= st.columns(5)
    with bcol1:
        pass
    with bcol2:
        pass
    with bcol3:
        pass
    with bcol4:
        pass
    with bcol5:
        on_press = st.button('generatoon', key='generation_button')
            
    if on_press:        
        '''
        background_file = st.file_uploader('Choose an image',
                                      type=['jpg', 'jpeg', 'png'],
                                      key='background',)
        '''
        # fig = plt.figure(figsize=(10, 10))
        background_image_bytes = background_file.getvalue()
        back_img = Image.open(BytesIO(background_image_bytes))
        draw = ImageDraw.Draw(back_img)
        for i, translated in enumerate(translated_list):
            font_type = ImageFont.truetype(os.path.join(font_path, font_list[i]), 20)
            print('font type:', font_type)
            draw.text((translated[0], translated[1]), translated[2], 'black',
            font=font_type,
            )
        print('draw: ', draw)
        print('type: ',type(back_img))
        st.image(back_img)

        