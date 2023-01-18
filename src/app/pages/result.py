import streamlit as st
from PIL import Image
import io

# def app():
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.title("Toon-ranslate")

cols = st.columns([1, 5, 1, 5, 1])
with cols[1]:
    st.markdown("<h3 style='text-align: center;'>원본</h3>", unsafe_allow_html=True)
    img_original = Image.open(
        "/opt/ml/level3_productserving-level3-cv-11/src/app/test_file/windbreaker_ko.PNG"
    )
    st.image(img_original)
with cols[3]:
    st.markdown("<h3 style='text-align: center;'>결과물</h3>", unsafe_allow_html=True)
    img_output = Image.open(
        "/opt/ml/level3_productserving-level3-cv-11/src/app/test_file/windbreaker_en.PNG"
    )
    st.image(img_output)

bcols = st.columns([5, 1, 1, 1, 5])
with bcols[1]:
    st.button("Edit")
with bcols[2]:
    st.button("Share")
with bcols[3]:
    with open(
        "/opt/ml/level3_productserving-level3-cv-11/src/app/test_file/windbreaker_en.PNG",
        "rb",
    ) as img_file:
        st.download_button(
            "Download", img_file, file_name="output.png", mime="image/png"
        )
