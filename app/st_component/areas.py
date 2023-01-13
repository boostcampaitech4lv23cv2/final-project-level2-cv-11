import io
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from models.translation import get_translate
from models.ocr import dummy_ocr

# initial_drawing object 템플릿
RECT = {'type': 'rect', 'version': '4.4.0', 'originX': 'left', 'originY': 'top', 'left': 0, 'top': 0, 'width': 0, 'height': 0, 'fill': 'rgba(255, 165, 0, 0.3)', 'stroke': '#eee', 'strokeWidth': 3, 'strokeDashArray': None, 'strokeLineCap': 'butt', 'strokeDashOffset': 0, 'strokeLineJoin': 'miter', 'strokeUniform': True, 'strokeMiterLimit': 4, 'scaleX': 1, 'scaleY': 1, 'angle': 0, 'flipX': False, 'flipY': False, 'opacity': 1, 'shadow': None, 'visible': True, 'backgroundColor': '', 'fillRule': 'nonzero', 'paintFirst': 'fill', 'globalCompositeOperation': 'source-over', 'skewX': 0, 'skewY': 0, 'rx': 0, 'ry': 0}

def anno_area(input_img, key):
    # 이미지 사이즈 변경
    img = Image.open(input_img)
    w, h = img.size
    canvas_width = 400
    canvas_height = h * (canvas_width / w)

    # ocr_flag 를 체크하고, 필요하면 OCR 수행
    if st.session_state[f'{key}_ocr_flag']:
        ocr_results = dummy_ocr(img)

        # OCR 결과를 initial_drawing 에 맞는 포맷으로 변환
        print(ocr_results)
        rects = []
        # TODO: OCR 결과는 원본 이미지의 좌표를 반환하므로, 캔버스의 크기에 맞게 변환해야함
        for i, result in enumerate(ocr_results):
            rect = RECT.copy()
            rect['left'] = result[0][0]
            rect['top'] = result[0][1]
            rect['width'] = result[1][0] - result[0][0]
            rect['height'] = result[1][1] - result[0][1]
            rects.append(rect)
            st.session_state[f'{key}_anno{i}'] = result[2] # OCR 텍스트를 session_state에 저장

        initial_drawing = {'objects': rects}
        st.session_state[f'{key}_initial_drawing'] = initial_drawing
        st.session_state[f'{key}_ocr_flag'] = False

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
        key=f'{key}_canvas',
        initial_drawing=st.session_state[f'{key}_initial_drawing'],
    )
    print(canvas_width)
    print(canvas_height)
    # annotation 값
    if canvas_result.json_data is not None:
        new_objects = canvas_result.json_data['objects']
        for i, obj in enumerate(new_objects):
            with st.expander(f'anntation {i}'):
                obj['text'] = st.text_input('인식된 글자', key=f'{key}_anno{i}')
                st.text(f"left:{int(obj['left']/canvas_width*w)}  top:{int(obj['top']*h/canvas_height)}  width:{int(obj['width']/canvas_width*w)}  height:{int(obj['height']*h/canvas_height)}  text:{obj['text']}")
                print(type(obj['left']))
                translation = get_translate(obj['text'])
                st.text_input('번역된 글자', translation, key=f'{key}_translated{i}')
    else:
        pass

def imag_show(img_file):
    background_image_bytes = img_file.getvalue()
    background_image = Image.open(io.BytesIO(background_image_bytes))
    st.image(background_image, caption='Uploaded Image')