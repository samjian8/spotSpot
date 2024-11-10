# Import modules here
import streamlit as st  # type: ignore
import cv2  # type: ignore
from PIL import Image  # type: ignore
import numpy as np  # type: ignore
import json
import base64
import torch
from torchvision import transforms, models

# Load the skincare recommendations from the file
with open("recommendations.txt", "r") as file:
    skincare_recommendations = json.load(file)
    
# Load the pre-trained model only once
num_classes = 7
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.shufflenet_v2_x0_5(pretrained=False)  # Use the model architecture you trained
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)  # Modify the final layer as needed
model.load_state_dict(torch.load('model.pth'))  # Load the saved model weights
model = model.to(device)  # Move the model to the correct device
model.eval()  # Set the model to evaluation mode

# Define image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def analyze_acne(image):
    # Convert numpy array to PIL Image and ensure RGB format
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Apply transformations
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    # Perform inference
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted_class = torch.max(outputs, 1)
    
    # Updated class labels
    classes = ['Blackheads', 'Clear Skin', 'Cystic', 'Papules', 'Pustules', 'Rosacea', 'Whiteheads']
    class_label = classes[predicted_class.item()]
    
    return class_label



# Page Title
st.set_page_config(page_title="spotSpot", page_icon="sslogo.png", layout="wide")

# Use Local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

# Load the image and convert it to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
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

# Convert your image to base64
image_base64 = get_base64_image("sslogo.png")  

st.markdown(
    f"""
    <style>
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 20px;
        background: linear-gradient(100deg, #1e4482, #537fad);
        border-radius: 30px;
        color: white;
        font-size: 18px;
        font-weight: bold;
        width: calc(100% - 20px);
        margin: 20px 0px;
    }}
    .header-left {{
        display: flex;
        align-items: center;
    }}
    .header-left img {{
        margin-right: 8px;
        width: 50px;
        height: 50px;
    }}
    </style>
    
    <div class="header-container">
        <div class="header-left">
            <img src="data:image/png;base64,{image_base64}" alt="Icon">
            spotSpot
        </div>
        <div class="header-right">
            spot the issue, treat with confidence
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: left; font-weight: bold;'>Welcome to spotSpot – your personal virtual dermatologist. Follow the instructions below to get started on your journey to healthier skin.</p>",
    unsafe_allow_html=True
)

with st.container():
    left_column, right_column = st.columns(2)
## fix the before
# Initialize session state variables if not already done
if "photo_captured" not in st.session_state:
    st.session_state.photo_captured = None
if "acne_issue" not in st.session_state:
    st.session_state.acne_issue = ""  # Initialize with an empty string


with left_column:
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

        if st.button("Generate Analysis Results"):
            # Check if a photo is captured or uploaded
            if st.session_state.photo_captured is not None:
                img = Image.open(st.session_state.photo_captured)
                img_array = np.array(img)  # Convert image to numpy array

                # Send the image to the backend for analysis and store the result in session state
                st.session_state.acne_issue = analyze_acne(img_array)
            else:
                st.error("Please capture or upload a photo first.")

with right_column:
    # Only display results if the acne issue has been detected (button was pressed and analysis ran)
    if st.session_state.acne_issue:
        issue = st.session_state.acne_issue

        # Retrieve data from skincare recommendations
        skincare_info = skincare_recommendations.get(issue, {})
        message = skincare_info.get("Message", "Keep up the good work!")
        skincare_routine = skincare_info.get("Routine", {})
        best_ingredients = skincare_info.get("Best Ingredients", [])
        avoid = skincare_info.get("Avoid", [])

        # Display skincare status and regimen based on the issue detected
        if issue == "Clear Skin":
            st.markdown(
                f"""
                <div class="right-column-container" style="background-color: #1e4482AA; border-radius: 15px; padding: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); height: 520px; overflow-y: auto;">
                    <div style="color: white; font-size: 22px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
                        Your Skin Status
                    </div>
                    <div style='font-size: 14px; color: white;'>{message}</div>
                    <br>
                    <div style="color: white; font-size: 22px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
                        Your Recommended Skincare Regimen
                    </div>
                    <div style="font-size: 20px; font-weight: bold;">Routine</div>
                    {"".join([f"<div style='font-size: 14px;'>- <strong>{step}</strong>: {description}</div>" for step, description in skincare_routine.items()])}
                    <div style="font-size: 20px; font-weight: bold;">Best Ingredients</div>
                    {"".join([f"<div style='font-size: 14px;'>- {ingredient}</div>" for ingredient in best_ingredients])}
                    <div style="font-size: 20px; font-weight: bold;">Avoid</div>
                    {"".join([f"<div style='font-size: 14px;'>- {item}</div>" for item in avoid])}       
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="right-column-container" style="background-color: #1e4482AA; border-radius: 15px; padding: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); height: 520px; overflow-y: auto;">
                    <div style="color: white; font-size: 22px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
                        Your Skin Issue(s)
                    </div>
                    <div style='font-size: 14px; color: white;'>
                        Detected Skin Issue: <strong>{issue}</strong>
                    </div>
                    <br>
                    <div style="color: white; font-size: 22px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
                        Your Recommended Skincare Regimen
                    </div>
                    <div style="font-size: 20px; font-weight: bold;">Routine</div>
                    {"".join([f"<div style='font-size: 14px;'>- <strong>{step}</strong>: {description}</div>" for step, description in skincare_routine.items()])}
                    <div style="font-size: 20px; font-weight: bold;">Best Ingredients</div>
                    {"".join([f"<div style='font-size: 14px;'>- {ingredient}</div>" for ingredient in best_ingredients])}
                    <div style="font-size: 20px; font-weight: bold;">Avoid</div>
                    {"".join([f"<div style='font-size: 14px;'>- {item}</div>" for item in avoid])}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        # Display headers with "No issue detected yet" placeholders
        st.markdown(
            """
            <div class="right-column-container" style="background-color: #1e4482AA; border-radius: 15px; padding: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); height: 520px; overflow-y: auto;">
                <div style="color: white; font-size: 22px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
                    Your Skin Issue(s)
                </div>
                <div style='font-size: 14px; color: white;'>
                    Follow the steps below to generate your skin issue(s).
                </div>
                <br>
                <div style="color: white; font-size: 22px; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 5px; margin-bottom: 15px;">
                    Your Recommended Skincare Regimen
                </div>
                <div style='font-size: 14px; color: white;'>Follow the steps below to generate your recommended skincare regimen.</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown(
    """
    <style>
    .dashed-line {
        width: 100%; /* Takes up full width of the container */
        border-top: 2px dashed #ccc; /* Adjust thickness and color as needed */
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with left_column:
    with st.container():
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')      
        st.subheader('''Effortlessly identify your acne type. ''')
        st.write('''
            spotSpot analyzes your skin with a simple photo capture, providing a clear diagnosis to guide your skincare journey. Knowing your acne type is the first step toward effective, personalized care.''')

    with st.container():
        st.subheader('''Follow the steps below to get started: ''')
        st.write('''
            \n1. Live Preview: Use the live camera feed to position your face. 
            \n2. Capture Photo: Click "Take Photo" to take a photo. 
            \n3. Recapture: If you’re not satisfied with the photo, click "Clear Photo" to try again. 
            \n4. Analyze: Once you’re happy with the photo, click "Generate Analysis Results" to send it for analysis. 
            \n5. Results: View the analysis results and get insights into your acne type and recommended treatments.''')
        
with right_column:
    image = Image.open("acnetypes.png")
    
    # CSS for centering the image in the container
    st.markdown(
        """
        <style>
        .fixed-height-image {
            height: 110px;  /* Set the total height of the container */
            display: flex;
            justify-content: center;  /* Centers the image horizontally */
            align-items: center;  /* Centers the image vertically */
            #padding-top: 20px;
            padding-bottom: 20px;
        }
        .fixed-height-image img {
            height: 300px;  /* Set the fixed height of the image */
            object-fit: contain;  /* Ensures the image scales proportionally */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Display the image within the centered container
st.markdown('<div class="fixed-height-image">', unsafe_allow_html=True)
st.image(image, use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)
