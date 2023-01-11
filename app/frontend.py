import streamlit as st
from PIL import Image
import io
from streamlit_drawable_canvas import st_canvas
import pandas as pd
from models.translation import get_translate

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.title('Generatoon!')


col1, col2, col3 = st.columns(3)

with col1:
   st.header("Background")
   background_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'], key='background',)
   if background_file:
        background_image_bytes = background_file.getvalue()
        background_image = Image.open(io.BytesIO(background_image_bytes))
        st.image(background_image, caption='Uploaded Image')

with col2:
    st.header("Typical Text")
    typical_image = st.file_uploader("Background image:", type=['jpg', 'jpeg', 'png'], key='Typical')
    if typical_image:
        img = Image.open(typical_image)
        w, h = img.size
        inner_width = 400
        canvas_width = inner_width
        canvas_height = h * (canvas_width / w)


    

        typical_canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=3,
        stroke_color="#eee",
        background_color="#eee",
        background_image=Image.open(typical_image) if typical_image else None,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode='rect',
        point_display_radius=0,
        key='typical_canvas'
        )

        if len(typical_canvas_result.json_data['objects']) > 0:
            typical_new_objects = typical_canvas_result.json_data['objects']
            for i, obj in enumerate(typical_new_objects):
                obj['text'] = st.text_input('', key=i)
                st.text(f"left:{obj['left']}  top:{obj['top']}  width:{obj['width']}  height:{obj['height']}  text:{obj['text']}")
        else:
            pass


with col3:
    st.header("UnTypical Text")
    untypical_image = st.file_uploader("Background image:", type=['jpg', 'jpeg', 'png'], key='UnTypical')
    if untypical_image:
        img = Image.open(untypical_image)
        w, h = img.size

        inner_width = 400
        canvas_width = inner_width
        canvas_height = h * (canvas_width / w)

        untypical_canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=3,
        stroke_color="#eee",
        background_color="#eee",
        background_image=Image.open(untypical_image) if untypical_image else None,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode='rect',
        point_display_radius=0,
        key='untypical_canvas'
        )

        if len(untypical_canvas_result.json_data['objects']) > 0:
            untypical_new_objects = untypical_canvas_result.json_data['objects']
            for i, obj in enumerate(untypical_new_objects):
                obj['text'] = st.text_input('', key='untypical'+str(i))
                st.text(f"left:{obj['left']}  top:{obj['top']}  width:{obj['width']}  height:{obj['height']}  text:{obj['text']}")
                translation = get_translate(obj['text'])
                st.text(translation)
        else:
            pass
        # pass

st.markdown("----", unsafe_allow_html=True)

if background_file and typical_image and untypical_image:
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
        st.button('generatoon', key='generation_button')

    