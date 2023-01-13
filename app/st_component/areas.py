import io
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

    flag = st.checkbox('편집', key=f'{key}_edit')
    drawing_mode = 'transform' if flag else 'rect'

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
        drawing_mode=drawing_mode,
        point_display_radius=0,
        key=f'{key}_canvas'
    )
    print(canvas_width)
    print(canvas_height)
    # annotation 값
    if canvas_result.json_data is not None:
        new_objects = canvas_result.json_data['objects']
        for i, obj in enumerate(new_objects):
            with st.expander(f'anntation {i}'):
                obj['text'] = st.text_input('인식된 글자', key=f'{key}_anno{str(i)}')
                st.text(f"left:{int(obj['left']/canvas_width*w)}  top:{int(obj['top']*h/canvas_height)}  width:{int(obj['width']/canvas_width*w)}  height:{int(obj['height']*h/canvas_height)}  text:{obj['text']}")
                print(type(obj['left']))
                translation = get_translate(obj['text'])
                st.text_input('번역된 글자', translation, key=f'{key}_translated{str(i)}')
    else:
        pass

def imag_show(img_file):
    background_image_bytes = img_file.getvalue()
    background_image = Image.open(io.BytesIO(background_image_bytes))
    st.image(background_image, caption='Uploaded Image')