import streamlit as st
from PIL import Image
from pathlib import Path

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.title("Toon-ranslate")

test_file = Path(__file__).parents[1] / "test_file"

cols = st.columns([1, 5, 1, 5, 1])
with cols[1]:
    st.markdown("<h3 style='text-align: center;'>원본</h3>", unsafe_allow_html=True)
    img_original = Image.open(test_file / "windbreaker_ko.PNG")
    st.image(img_original)
with cols[3]:
    st.markdown("<h3 style='text-align: center;'>결과물</h3>", unsafe_allow_html=True)
    img_output = Image.open(test_file / "windbreaker_en.PNG")
    st.image(img_output)

bcols = st.columns([5, 1, 1, 1, 5])
with bcols[1]:
    st.button("Edit")
with bcols[2]:
    st.button("Share")
with bcols[3]:
    with open(test_file / "windbreaker_en.PNG", "rb") as img_file:
        st.download_button(
            "Download", img_file, file_name="output.png", mime="image/png"
        )
