import streamlit as st
from mask_pan import mask_pan

# Page setup
st.set_page_config(page_title="Secure PAN Redaction System", layout="wide")

# ---------- Title ----------
st.markdown(
"""
<h1 style='text-align:center; font-size:60px;'>
🔒 Secure PAN Redaction System
</h1>
<h3 style='text-align:center;'>
Upload PAN card image and automatically mask the PAN number
</h3>
""",
unsafe_allow_html=True
)

# ---------- Upload ----------
uploaded_file = st.file_uploader(
"Upload PAN Card Image",
type=["jpg","jpeg","png"]
)

# ---------- Process Image ----------
if uploaded_file is not None:

    # Save uploaded file
    with open("temp.png","wb") as f:
        f.write(uploaded_file.getbuffer())

    # Detect and mask PAN
    original_pan, masked_pan, result_img = mask_pan("temp.png")

    if original_pan:

        st.success("PAN detected and masked successfully")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(uploaded_file, use_container_width=True)

        with col2:
            st.subheader("Masked Image")
            st.image(result_img, use_container_width=True)

        st.write("")

        # Download button
        with open(result_img,"rb") as file:
            st.download_button(
                label="Download Masked Image",
                data=file,
                file_name="masked_pan.png",
                mime="image/png"
            )

    else:
        st.error("PAN number not detected in the image")