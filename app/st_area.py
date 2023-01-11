import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from models.translation import get_translate

def anno_area(input_img, key):
    # 이미지 사이즈 변경
    img = Image.open(input_img)
    w, h = img.size
    canvas_width = 400
    canvas_height = h * (canvas_width / w)

    # 캔버스
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=3,
        stroke_color="#eee",
        background_color="#eee",
        background_image=img,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode='rect',
        point_display_radius=0,
        key=f'{key}_canvas'
    )

    # annotation 값
    if canvas_result.json_data is not None:
        new_objects = canvas_result.json_data['objects']
        for i, obj in enumerate(new_objects):
            with st.expander(f'anntation {i}'):
                obj['text'] = st.text_input('인식된 글자', key=f'{key}_anno{str(i)}')
                st.text(f"left:{obj['left']}  top:{obj['top']}  width:{obj['width']}  height:{obj['height']}  text:{obj['text']}")
                translation = get_translate(obj['text'])
                st.text_input('번역된 글자', translation, key=f'{key}_translated{str(i)}')
    else:
        pass