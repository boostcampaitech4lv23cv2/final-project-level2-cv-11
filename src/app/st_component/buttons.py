import streamlit as st
from streamlit_extras.switch_page_button import switch_page


def btn_generation():
    bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
    with bcol1:
        pass
    with bcol2:
        pass
    with bcol3:
        pass
    with bcol4:
        pass
    with bcol5:
        if st.button("generatoon", key="generation_button"):
            switch_page("result")
