import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import io
from io import BytesIO
import numpy as np
import os


## 폰트 파일 위치
font_path = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ),
    "data",
    "fonts",
    "typical",
)


def btn_generation(background_file, translated_list, font_list):
    bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
    with bcol1:
        pass
    with bcol2:
        pass
    with bcol3:
        pass
    with bcol4:
        pass
    with bcol5:
        on_press = st.button("generatoon", key="generation_button")

    if on_press:
        """
        background_file = st.file_uploader('Choose an image',
                                      type=['jpg', 'jpeg', 'png'],
                                      key='background',)
        """
        # fig = plt.figure(figsize=(10, 10))
        background_image_bytes = background_file.getvalue()
        back_img = Image.open(BytesIO(background_image_bytes))
        draw = ImageDraw.Draw(back_img)
        for i, translated in enumerate(translated_list):
            font_type = ImageFont.truetype(os.path.join(font_path, font_list[0]), 20)
            draw.text(
                (translated[0], translated[1]),
                translated[2],
                "black",
                font=font_type,
            )
        st.image(back_img)
