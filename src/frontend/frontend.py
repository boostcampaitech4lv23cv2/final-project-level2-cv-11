import streamlit as st
from st_component import areas as st_area
from st_component import buttons as st_buttons
from typing import Literal

# 각 모델 사용할 때
# model.Clova_OCR
# model.Papago_MT
# model.Tesseract_OCR
# model.Typical_FC 로 사용하면 됨


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
        try:
            translated_list, st.session_state.font_list = st_area.anno_area(
                typical_image, "typical"
            )
        except:
            pass

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

if background_file and typical_image:
    try:
        st_buttons.btn_generation(
            background_file, translated_list, st.session_state.font_list
        )
    except:
        pass
