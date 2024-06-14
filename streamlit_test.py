import streamlit as st
import cv2
import os

st.set_page_config(layout="wide", page_title="image_dropdown")

st.title("Drop Down")

def load_image(file_path):
    if os.path.exists(file_path):
        image = cv2.imread(file_path)
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return image_rgb
        else:
            st.error(f"Error loading image: {file_path}")
            return None
    else:
        st.error(f"File not found: {file_path}")
        return None

# Define image paths and captions
images_info = {
    "image 0": "3_HUAWEI-NOVA-LITE_S.jpg",
    "image 1": "2_XIAOMI-PROCOFONE-F1_S.jpg",
    "image 2": "1_XIAOMI-PROCOFONE-F1_S.jpg",
    "image 3": "0_IPHONE-SE_S.JPG"
}

# Create the selectbox with image captions
selected_caption = st.selectbox(label="Choose image", options=list(images_info.keys()))

# Load and display the selected image
if selected_caption:
    selected_image_path = images_info[selected_caption]
    selected_image = load_image(selected_image_path)
    if selected_image is not None:
        st.image(selected_image, caption=selected_caption, width=300)
