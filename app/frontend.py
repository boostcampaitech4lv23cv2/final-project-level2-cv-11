import streamlit as st
from PIL import Image
import io


st.set_page_config(layout="wide")

st.title('Generatoon!')


col1, col2, col3 = st.columns(3)

with col1:
   st.header("Background")
   background_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'], key='background')
   if background_file:
        background_image_bytes = background_file.getvalue()
        background_image = Image.open(io.BytesIO(background_image_bytes))
        st.image(background_image, caption='Uploaded Image')

with col2:
   st.header("Typical Text")
   typical_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'], key='typical')
   if typical_file:
        typical_image_bytes  = typical_file.getvalue()
        typical_image = Image.open(io.BytesIO(typical_image_bytes))
        st.image(typical_image, caption='Uploaded Image')
        st.button('annotation', key='typical_annotation')

with col3:
   st.header("UnTypical Text")
   untypical_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'], key='untypical')
   if untypical_file:
        untypical_image_bytes  = untypical_file.getvalue()
        untypical_image = Image.open(io.BytesIO(untypical_image_bytes))
        st.image(untypical_image, caption='Uploaded Image')
        st.button('annotation', key='untypical_annotation')

if background_file and typical_file and untypical_file:
    st.button('generatoon', key='generation_button')