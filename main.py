# Import modules here
import streamlit as st  # type: ignore
import cv2  # type: ignore
from PIL import Image  # type: ignore
import numpy as np  # type: ignore


# Page Title
st.set_page_config(page_title="spotSpot", page_icon="sslogo.png", layout="wide")

# Use Local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

def analyze_acne(image):
    # Dummy function to simulate backend analysis
    return "Acne Type: Example Type"

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 5rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 537fad 1e4482 31317d
with st.container():
    st.markdown(
        """
        <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 20px;
            background: linear-gradient(100deg, #1e4482, #537fad); /* Gradient colors */
            border-radius: 30px;
            color: white;
            font-size: 18px;
            font-weight: bold;
            width: calc(100% - 20px); /* Full width minus 10px margin on each side */
            margin: 20px 0px; /* 10px margin on left and right */
            box-sizing: border-box; /* Include padding and border in the element's total width */
        }
        .header-left {
            text-align: left;
        }
        .header-right {
            text-align: right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="header-container">
        <div class="header-left">spotSpot</div>
        <div class="header-right">spot the issue, treat with confidence</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: left; font-weight: bold;'>Welcome to SpotSpot – your personal virtual dermatologist. Follow the instructions below to get started on your journey to healthier skin.</p>",
    unsafe_allow_html=True
)

with st.container():
    left_column, right_column = st.columns(2)

with right_column:
    st.markdown(
        """
        <div style="color: white; font-size: 24px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
            -> Your Skincare Issues
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="color: white; font-size: 24px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
            -> Your Recommended Skincare Regimen
        </div>
        """,
        unsafe_allow_html=True
    )

with left_column:
    # Initialize session states if not already done
    if "photo_captured" not in st.session_state:
        st.session_state.photo_captured = None

    with st.container():
        # Option to take a photo using the camera
        camera = st.camera_input("Take a close up of the problem spots on your face.")

        # Option to upload an image
        uploaded_file = st.file_uploader("Or upload an image file...", type=["jpg", "png", "jpeg"])

        # Use camera input if available, otherwise use uploaded file
        if camera is not None:
            st.session_state.photo_captured = camera
        elif uploaded_file is not None:
            st.session_state.photo_captured = uploaded_file

        if st.button("Analyze"):
            # Check if a photo is captured or uploaded
            if st.session_state.photo_captured is not None:
                img = Image.open(st.session_state.photo_captured)
                img_array = np.array(img) # do testing to make sure it is takign the image that exists

                # Send the image to the backend for analysis (dummy function here)
                result = analyze_acne(img_array)

                # Display the result
                st.write("Analysis Result:")
                st.write(result)
            else:
                st.error("Please capture or upload a photo first.")

with st.container():
    st.subheader('''Follow the steps below to get started: ''')
    st.write('''
        \n1. Live Preview: Use the live camera feed to position your face. 
        \n2. Capture Photo: Click the “Capture” button to take a photo. 
        \n3. Recapture: If you’re not satisfied with the photo, click "Clear Photo" to try again. 
        \n4. Analyse: Once you’re happy with the photo, click “Analyze” to send it for analysis. 
        \n5. Results: View the analysis results and get insights into your acne type.''')