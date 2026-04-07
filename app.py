import streamlit as st
from mask_pan import mask_pan
from PIL import Image

st.title("Secure PAN Redaction System")

uploaded_file = st.file_uploader("Upload PAN Image", type=["jpg","png","jpeg"])

if uploaded_file:

    image = Image.open(uploaded_file)

    masked_image, pan = mask_pan(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image)

    with col2:
        st.subheader("Masked Image")
        st.image(masked_image)

    if pan:
        st.success("PAN detected and masked successfully")
        st.write("Detected PAN:", pan)
    else:
        st.error("PAN not detected")                  
