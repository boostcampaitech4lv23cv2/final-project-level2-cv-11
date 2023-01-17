import streamlit as st
from st_component import areas as st_area
from st_component import buttons as st_buttons

import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
import model
from pipeline import typical_pipeline

# 각 모델 사용할 때
# model.Clova_OCR
# model.Papago_MT
# model.Tesseract_OCR
# model.Typical_FC 로 사용하면 됨

# 이미지가 업로드 될 때마다 호출되는 콜백함수
# '(un)typical_ocr_flag' 를 True로 설정함
def set_ocr_flag(key):
    """
    이미지가 업로드 될 때마다 호출되는 콜백함수
    '(un)typical_ocr_flag' 를 True로 설정함
    """
    st.session_state[key] = True

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.title('Generatoon!')

col1, col2, col3 = st.columns(3)

with col1:
   st.header("Background")
   background_file = st.file_uploader('Choose an image',
                                      type=['jpg', 'jpeg', 'png'],
                                      key='background',)
   if background_file:
       st_area.imag_show(background_file)

with col2:
    st.header("Typical Text")
    typical_image = st.file_uploader("Background image:",
                                     type=['jpg', 'jpeg', 'png'],
                                     key='typical_uploader',
                                     on_change=set_ocr_flag,
                                     args=('typical_ocr_flag',))
    # TODO: 나중에 ocr_results는 함수 바깥에서 받아와야함, ex anno_area(input_img, key, ocr_results)
    if typical_image:
        Typical_pipeline = typical_pipeline.Typical_Pipeline()
        clova_result = Typical_pipeline.clova_ocr(typical_image.getvalue())
        st_area.anno_area(typical_image, 'typical', clova_result)
        mt_result = Typical_pipeline.papago(clova_result)
        print(mt_result)
    
    # clova_result = [[[555, 417], [958, 545], '서른다섯 배, 오백만 주로 계약했다.']]
    # mt_result = [[[555, 417], [958, 545], '서른다섯 배, 오백만 주로 계약했다.', 'Thirty-five times, five million shares signed.']]

with col3:
    st.header("UnTypical Text")
    untypical_image = st.file_uploader("Background image:",
                                       type=['jpg', 'jpeg', 'png'],
                                       key='untypical_uploader',
                                       on_change=set_ocr_flag,
                                       args=('untypical_ocr_flag',))
    if untypical_image:
        st_area.anno_area(untypical_image, 'untypical')


st.markdown("----", unsafe_allow_html=True)

if background_file and typical_image and untypical_image:
    st_buttons.btn_generation()