import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

# Apply yellow background style
st.markdown(
    """
    <style>
    body {
        background-color: #FFFFE0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to find the primary color in an image
def get_dominant_color(image, k=1):
    image = cv2.resize(image, (50, 50))
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
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

# Define matching rules and compatibility score
matching_rules = {
    ("blue", "brown"): 85,
    ("blue", "gray"): 80,
    ("black", "white"): 90,
    ("white", "black"): 90,
    ("red", "black"): 75,
    ("gray", "black"): 70,
    ("green", "khaki"): 80,
    ("blue", "white"): 85,
}

def match_clothing(color1, color2):
    return matching_rules.get((color1, color2)) or matching_rules.get((color2, color1), 0)

# Initialize session state for favorites
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# Streamlit App
st.title("Clothing and Accessories Match Checker")
st.write("Upload images of clothing and accessories to see if they match!")

# Image upload widgets for clothing items
img1_file = st.file_uploader("Choose first clothing image (e.g., shirt)", type=["jpg", "jpeg", "png"])
img2_file = st.file_uploader("Choose second clothing image (e.g., pants)", type=["jpg", "jpeg", "png"])

# Checkbox for adding to favorites, only shown if images are uploaded
add_to_favorites_checkbox = None
if img1_file and img2_file:
    add_to_favorites_checkbox = st.checkbox("Add this combination to favorites")

# Match button to trigger compatibility calculation
if img1_file and img2_file:
    if st.button("Match"):
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
        
        # Get compatibility score and display it
        match_score = match_clothing(color1_name, color2_name)
        if match_score > 0:
            st.write(f"### Compatibility: {match_score}%")
            is_match = True
        else:
            st.write("### Compatibility: 0% (No match)")
            is_match = False

        # If user selected checkbox, add to favorites
        if add_to_favorites_checkbox and is_match:
            favorite_combo = f"{color1_name} and {color2_name}"
            st.session_state["favorites"].append(favorite_combo)
            st.success("Outfit combo added to favorites!")

# Accessory upload section in an expandable container
with st.expander("Upload Accessories (e.g., shoes, belts)"):
    accessory_files = st.file_uploader("Choose accessory images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if accessory_files and img1_file and img2_file:
        for acc_file in accessory_files:
            acc_image = Image.open(acc_file)
            acc_image_cv = cv2.cvtColor(np.array(acc_image), cv2.COLOR_RGB2BGR)
            
            acc_color_rgb = get_dominant_color(acc_image_cv)
            acc_color_name = color_name(acc_color_rgb)
            
            st.write(f"Detected Color for Accessory: {acc_color_name}")
            
            # Calculate and display match percentage with main outfit
            acc_match_score = (match_clothing(acc_color_name, color1_name) + match_clothing(acc_color_name, color2_name)) // 2
            st.write(f"Accessory Compatibility: {acc_match_score}%")

# Favorite outfits dropdown
with st.expander("Favorite Outfit Combinations"):
    if st.session_state["favorites"]:
        st.write("Your favorite outfit combinations:")
        for favorite in st.session_state["favorites"]:
            st.write(f"• {favorite}")
    else:
        st.write("No favorite outfits saved yet.")
