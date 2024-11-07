import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

# Apply red background style
st.markdown(
    """
    <style>
    body {
        background-color: #FF0000;
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

# Map RGB color to common color names
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

# Define matching rules and compatibility scores
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

def calculate_compatibility_score(color1, color2):
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

# Display "Match" button and process images if button is clicked
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
        
        # Calculate compatibility score and display it
        match_score = calculate_compatibility_score(color1_name, color2_name)
        if match_score > 0:
            st.write(f"### Compatibility: {match_score}%")
            is_match = True
        else:
            st.write("### Compatibility: 0% (No match)")
            is_match = False

        # Display "Add to Favorites" checkbox only after matching is complete
        add_to_favorites_checkbox = st.checkbox("Add this combination to favorites")

        # If "Add to Favorites" is checked, add the combination and images to favorites
        if add_to_favorites_checkbox and is_match:
            st.session_state["favorites"].append({
                "colors": f"{color1_name} and {color2_name}",
                "img1": img1,
                "img2": img2
            })
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
            acc_match_score = (calculate_compatibility_score(acc_color_name, color1_name) + calculate_compatibility_score(acc_color_name, color2_name)) // 2
            st.write(f"Accessory Compatibility: {acc_match_score}%")

# Favorite outfits dropdown with stored images
with st.expander("Favorite Outfit Combinations"):
    if st.session_state["favorites"]:
        st.write("Your favorite outfit combinations:")
        
        for idx, favorite in enumerate(st.session_state["favorites"]):
            st.write(f"• {favorite['colors']}")
            st.image(favorite["img1"], caption="Clothing Item 1")
            st.image(favorite["img2"], caption="Clothing Item 2")
            
            # "Delete Outfit Image" button
            if st.button(f"Delete Outfit Image {idx + 1}"):
                st.session_state["favorites"].pop(idx)
                st.experimental_rerun()  # Refresh the app after deletion
    else:
        st.write("No favorite outfits saved yet.")
