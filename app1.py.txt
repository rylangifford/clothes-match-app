import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Helper function to process images and determine if they match based on color similarity
def images_match(img1, img2, threshold=30):
    # Resize images to the same size for easier comparison
    img1 = cv2.resize(img1, (100, 100))
    img2 = cv2.resize(img2, (100, 100))
    
    # Convert images to the HSV color space for better color comparison
    img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    
    # Calculate the color histogram for each image
    hist_img1 = cv2.calcHist([img1_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist_img2 = cv2.calcHist([img2_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    
    # Normalize histograms
    cv2.normalize(hist_img1, hist_img1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist_img2, hist_img2, 0, 1, cv2.NORM_MINMAX)
    
    # Compare histograms using the correlation method
    similarity = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
    
    # Return True if similarity is above a certain threshold
    return similarity * 100 > threshold

# Streamlit UI
st.title("Clothing Match Checker")
st.write("Upload two images of clothing to see if they match!")

# Image upload widgets
img1_file = st.file_uploader("Choose first clothing image", type=["jpg", "jpeg", "png"])
img2_file = st.file_uploader("Choose second clothing image", type=["jpg", "jpeg", "png"])

if img1_file and img2_file:
    # Open the images with PIL, then convert to OpenCV format
    img1 = Image.open(img1_file)
    img2 = Image.open(img2_file)
    
    img1_cv = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    img2_cv = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)

    # Display images side-by-side
    st.image([img1, img2], caption=["First Image", "Second Image"], width=300)

    # Check if the images match
    if images_match(img1_cv, img2_cv):
        st.write("### 👍 The clothes match!")
    else:
        st.write("### 👎 The clothes don't match.")

