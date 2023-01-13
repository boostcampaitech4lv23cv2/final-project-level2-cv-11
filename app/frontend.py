import streamlit as st
from st_component import areas as st_area
from st_component import buttons as st_buttons

# 이미지가 업로드 될 때마다 호출되는 콜백함수
# '(un)typical_ocr_flag' 를 True로 설정함
def set_ocr_flag(key):
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
    if typical_image:
        st_area.anno_area(typical_image, 'typical')

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