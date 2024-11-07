import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

# Function to find the primary color in an image
def get_dominant_color(image, k=1):
    # Resize the image to reduce computation
    image = cv2.resize(image, (50, 50))
    # Reshape the image to a list of pixels
    pixels = image.reshape(-1, 3)
    # Use KMeans to find the dominant color
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    # Return the dominant color as the cluster center
    dominant_color = kmeans.cluster_centers_[0]
    return dominant_color

# Map RGB color to common color names (simplified)
def color_name(rgb_color):
    r, g, b = rgb_color
    if r > 150 and g < 100 and b < 100:
        return "red"
    elif r < 100 and g > 150 and b < 100:
        return "green"
    elif r < 100 and g < 100 and b > 150:
        return "blue"
    elif r > 150 and g > 150 and b < 100:
        return "yellow"
    elif r > 150 and g > 100 and b < 50:
        return "orange"
    elif r > 100 and g > 100 and b > 100:
        return "gray"
    elif r < 50 and g < 50 and b < 50:
        return "black"
    else:
        return "unknown"

# Define matching rules
matching_rules = {
    ("blue", "brown"): True,
    ("blue", "gray"): True,
    ("black", "white"): True,
    ("white", "black"): True,
    ("red", "black"): True,
    ("gray", "black"): True,
    ("green", "khaki"): True,
    ("blue", "white"): True,
    # Add more combinations as needed
}

def match_clothing(color1, color2):
    # Check both combinations
    return matching_rules.get((color1, color2)) or matching_rules.get((color2, color1))

# Streamlit App
st.title("Fashion Match Checker")
st.write("Upload images of clothing and accessories to see if they match!")

# Image upload widgets for clothing items
img1_file = st.file_uploader("Choose first clothing image (e.g., shirt)", type=["jpg", "jpeg", "png"])
img2_file = st.file_uploader("Choose second clothing image (e.g., pants)", type=["jpg", "jpeg", "png"])

# Accessory upload section in an expandable container
with st.expander("Upload Accessories (e.g., shoes, belts)"):
    accessory_files = st.file_uploader("Choose accessory images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if img1_file and img2_file:
    # Process clothing images
    img1 = Image.open(img1_file)
    img2 = Image.open(img2_file)
    
    img1_cv = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    img2_cv = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
    
    color1_rgb = get_dominant_color(img1_cv)
    color2_rgb = get_dominant_color(img2_cv)
    
    color1_name = color_name(color1_rgb)
    color2_name = color_name(color2_rgb)
    
    st.write(f"Detected Colors for Clothing: {color1_name} and {color2_name}")
    
    # Check clothing match
    if match_clothing(color1_name, color2_name):
        st.write("### 👍 The clothes match!")
    else:
        st.write("### 👎 The clothes don't match.")

    # Process accessory images if any
    if accessory_files:
        accessory_colors = []
        
        for acc_file in accessory_files:
            acc_image = Image.open(acc_file)
            acc_image_cv = cv2.cvtColor(np.array(acc_image), cv2.COLOR_RGB2BGR)
            
            acc_color_rgb = get_dominant_color(acc_image_cv)
            acc_color_name = color_name(acc_color_rgb)
            accessory_colors.append(acc_color_name)
            
            st.write(f"Detected Color for Accessory: {acc_color_name}")
            
            # Check if each accessory matches the clothing items
            if match_clothing(acc_color_name, color1_name) and match_clothing(acc_color_name, color2_name):
                st.write("### 👍 Accessory matches both clothing items!")
            else:
                st.write("### 👎 Accessory doesn't match both clothing items.")
