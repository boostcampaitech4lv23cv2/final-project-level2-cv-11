import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import io
from io import BytesIO
import numpy as np
def btn_generation(background_file, translated_list):
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
        on_press = st.button('generatoon', key='generation_button')
            
    if on_press:        
        fig, ax = plt.subplots(figsize=(5, 5))
        # fig = plt.figure(figsize=(10, 10))
        background_image_bytes = background_file.getvalue()
        back_img = Image.open(BytesIO(background_image_bytes))
        ax.imshow(np.asarray(back_img))
        for translated in translated_list:
            ax.text(x=translated[0], y=translated[1], s=translated[2],)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.pyplot(fig)

        