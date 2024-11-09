# import modules here
import streamlit as st # type: ignore
import cv2 # type: ignore
from PIL import Image # type: ignore
import numpy as np # type: ignore

# Page Title
st.set_page_config(page_title="spotSpot", page_icon="sslogo.png", layout="wide")

# Use Local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")
with st.container():
    # Header Section
    st.subheader("spotSpot")

    # Content
    st.title("Welcome to Acne Type Identifier")
    st.write("Discover Your Acne Type with Ease")
    st.write('''Our app helps you identify the type of acne you have by simply capturing a photo. 
             \nUnderstanding your acne type is the first step towards effective treatment and clearer skin.''')
    st.write("---")

with st.container():
    left_column, right_column = st.columns(2)

with left_column:
    st.subheader('''Follow the steps below to get started: ''')
    st.write('''
        \n1. Live Preview: Use the live camera feed to position your face. 
        \n2. Capture Photo: Click the “Capture” button to take a photo. 
        \n3. Recapture: If you’re not satisfied with the photo, click “Recapture” to try again. 
        \n4. Analyse: Once you’re happy with the photo, click “Analyse” to send it for analysis. 
        \n5. Results: View the analysis results and get insights into your acne type.''')


with right_column:
    # Live preview
    camera = st.camera_input("")

    if camera:
        # Display captured photo
        st.image(camera, caption="Captured Photo", use_column_width=True)
    
        # Buttons for recapture and analyze
        if st.button("Recapture"):
            st.experimental_rerun()
    
        if st.button("Analyse"):
        # Convert the image to a format suitable for the backend
            img = Image.open(camera)
            img_array = np.array(img)
        
            # Send the image to the backend for analysis (dummy function here)
            result = analyze_acne(img_array)
        
            # Display the result
            st.write("Analysis Result:")
            st.write(result)    

def analyze_acne(image):
    # Dummy function to simulate backend analysis
    return "Acne Type: Example Type"