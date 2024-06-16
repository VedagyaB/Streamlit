import streamlit as st
import cv2
import os
import numpy as np
from cleanvision.imagelab import Imagelab
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Image Grid")

st.title("Image Grid")

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

def get_images_from_directory(directory):
    images_info = {}
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(directory, filename)
                caption = os.path.splitext(filename)[0]
                images_info[caption] = file_path
    else:
        st.error(f"Directory not found: {directory}")
    return images_info

# Function to select directories using multiselect
def select_directories():
    # List all directories in current working directory
    directories = [name for name in os.listdir() if os.path.isdir(name)]
    selected_directories = st.multiselect("Select directories", directories)
    return selected_directories

# Get selected directories from dropdown
selected_directories = select_directories()

# Display images from selected directories in a matrix layout
# if selected_directories:
#     for directory in selected_directories:
#         st.header(f"Images in directory '{directory}':")
#         images_info = get_images_from_directory(directory)
        
#         if images_info:
#             num_columns = int(np.sqrt(len(images_info)))  # Adjust columns based on number of images
            
#             # Create the grid
#             rows = len(images_info) // num_columns + (len(images_info) % num_columns > 0)
#             for row in range(rows):
#                 cols = st.columns(num_columns)
#                 for col_index in range(num_columns):
#                     image_index = row * num_columns + col_index
#                     if image_index < len(images_info):
#                         image = load_image(list(images_info.values())[image_index])
#                         if image is not None:
#                             cols[col_index].image(image, use_column_width=True)
#         else:
#             st.error(f"No images found in directory '{directory}'.")

    # Select issues to analyze with CleanVision
issues = {"blurry", "near_duplicates","exact_duplicate"}
selected_issues = st.multiselect("Select issues", issues)

if selected_issues:
        # Instantiate Imagelab for each selected directory
    for directory in selected_directories:
        lab = Imagelab(directory)
        lab.find_issues()
        report = lab.report(issue_types=selected_issues)
        st.write(f"Issues report for directory '{directory}':")
        st.write(report)
        plt.savefig("report.png")
        st.image("report.png")
        plt.close()
else:
    st.warning("Please select one or more directories from the dropdown.")
