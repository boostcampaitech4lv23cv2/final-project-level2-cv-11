import streamlit as st
from st_component import areas as st_area
from st_component import buttons as st_buttons
from typing import Literal
import io
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import requests
from typing import Literal

translated_list = 0
# initial_drawing object 템플릿
# fmt: off
RECT = {'type': 'rect', 'version': '4.4.0', 'originX': 'left', 'originY': 'top', 'left': 0, 'top': 0, 'width': 0, 'height': 0, 'fill': 'rgba(255, 165, 0, 0.3)', 'stroke': '#eee', 'strokeWidth': 3, 'strokeDashArray': None, 'strokeLineCap': 'butt', 'strokeDashOffset': 0, 'strokeLineJoin': 'miter', 'strokeUniform': True, 'strokeMiterLimit': 4, 'scaleX': 1, 'scaleY': 1, 'angle': 0, 'flipX': False, 'flipY': False, 'opacity': 1, 'shadow': None, 'visible': True, 'backgroundColor': '', 'fillRule': 'nonzero', 'paintFirst': 'fill', 'globalCompositeOperation': 'source-over', 'skewX': 0, 'skewY': 0, 'rx': 0, 'ry': 0}


def set_ocr_flag(key: Literal["typical", "untypical"]):
    """
    이미지가 업로드 될 때마다 호출되는 콜백함수
    '(un)typical_ocr_flag' 를 True로 설정함
    """
    st.session_state[f"{key}_ocr_flag"] = True


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.title("Generatoon!")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Background")
    background_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        key="background",
    )
    if background_file:
        background_image = st_area.imag_show(background_file)

with col2:
    st.header("Typical Text")
    typical_image = st.file_uploader(
        "Background image:",
        type=["jpg", "jpeg", "png"],
        key="typical_uploader",
        on_change=set_ocr_flag,
        args=("typical",),
    )
    if typical_image:
        img = Image.open(typical_image)
        w, h = img.size
        canvas_width = 400
        canvas_height = h * (canvas_width / w)

        # OCR 한번만 실행
        if st.session_state["typical_ocr_flag"]:
            # OCR inference
            image_bytes = typical_image.getvalue()
            files = {'file': image_bytes}
            txt_res = requests.post('http://localhost:30002/txt_extraction', files=files).json()
            ocr_results = txt_res["ocr_result"]
            print(txt_res)
            st.session_state.font_list = txt_res["font_result"]
            # initial_drawing 포맷으로 변환
            rects = []
            for i, result in enumerate(ocr_results):
                rect = RECT.copy()
                rect["left"] = result[0][0] / w * canvas_width
                rect["top"] = result[0][1] / h * canvas_height
                rect["width"] = (result[1][0] - result[0][0]) / w * canvas_width
                rect["height"] = (result[1][1] - result[0][1]) / h * canvas_height
                rects.append(rect)
                st.session_state["typical_anno{i}"] = result[2]  # OCR 텍스트를 session_state에 저장

            initial_drawing = {"objects": rects}
            st.session_state[f"typical_initial_drawing"] = initial_drawing
            st.session_state[f"typical_ocr_flag"] = False

        flag = st.checkbox("편집", key="typical_edit")
        drawing_mode = "transform" if flag else "rect"

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
            key="typical_canvas",
            initial_drawing=st.session_state[f"typical_initial_drawing"],
        )

        # annotation 값
        if canvas_result.json_data is not None:
            new_objects = canvas_result.json_data['objects']
            translated_list = []
            for i, obj in enumerate(new_objects):
                with st.expander(f"anntation {i}"):
                    obj["text"] = st.text_input("인식된 글자", key="typical_anno{i}")
                    st.text(
                        f"left:{int(obj['left']/canvas_width*w)}  top:{int(obj['top']*h/canvas_height)}  width:{int(obj['width']/canvas_width*w)}  height:{int(obj['height']*h/canvas_height)}  text:{obj['text']}"
                    )
                    params = {"text": f"{obj['text']}"}
                    r = requests.post(f"http://localhost:30002/mt", params=params)
                    translation = r.json() if r.status_code == 200 else ""
                    st.text_input("번역된 글자", translation, key="typical_translated{i}")
                    translated_list.append([int(obj['left']/canvas_width*w), int(obj['top']*h/canvas_height), translation])

with col3:
    st.header("UnTypical Text")
    untypical_image = st.file_uploader(
        "Background image:",
        type=["jpg", "jpeg", "png"],
        key="untypical_uploader",
        on_change=set_ocr_flag,
        args=("untypical",),
    )
    if untypical_image:
        st_area.anno_area(untypical_image, "untypical")


st.markdown("----", unsafe_allow_html=True)

if background_file and typical_image and type(translated_list) == list:
    print('확인', st.session_state.font_list)
    st_buttons.btn_generation(
        background_file, translated_list, st.session_state.font_list
    )
