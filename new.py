import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the page
st.set_page_config(page_title="AI Image Editor", layout="wide")
st.title("🎨 AI Image Editor with Gemini")

# Initialize Gemini client
@st.cache_resource
def init_gemini():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # Pass as string

client = init_gemini()

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    edit_prompt = st.text_area(
        "Edit instructions",
        value="Add a beautiful tree in the background",
        help="Describe what changes you want to make to the image"
    )
    generate_mode = st.radio(
        "Mode",
        ["Edit Existing Image", "Generate New Image"],
        index=0
    )
    
    if generate_mode == "Generate New Image":
        creation_prompt = st.text_area(
            "Image description",
            value="A 3D rendered image of a pig with wings and a top hat flying over a happy futuristic sci-fi city with lots of greenery",
            help="Describe the image you want to generate"
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload an image to edit",
            type=["png", "jpg", "jpeg"]
        )

    submit_button = st.button("Process Image")

# Main content area
col1, col2 = st.columns(2)

if submit_button:
    with st.spinner("Generating your image..."):
        try:
            if generate_mode == "Generate New Image":
                # Generate new image
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=[creation_prompt],
                    config=types.GenerateContentConfig(
                        response_modalities=['Text', 'Image']
                    )
                )
            else:
                if uploaded_file is None:
                    st.warning("Please upload an image first")
                    st.stop()
                
                # Edit existing image
                image = Image.open(uploaded_file)
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=[
                        edit_prompt,
                        image
                        # types.Part.from_data(img_bytes, mime_type="image/png")
                    ],
                    config=types.GenerateContentConfig(
                        response_modalities=['Text', 'Image']
                    )
                )

            # Display results
            with col1:
                st.subheader("Original Image" if generate_mode == "Edit Existing Image" else "Prompt")
                if generate_mode == "Edit Existing Image":
                    st.image(uploaded_file, use_container_width=True)
                else:
                    st.write(creation_prompt)

            with col2:
                st.subheader("Result")
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        st.write(part.text)
                    elif part.inline_data is not None:
                        img = Image.open(BytesIO(part.inline_data.data))
                        st.image(img, use_container_width=True)
                        
                        # Add download button
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button(
                            label="Download Image",
                            data=byte_im,
                            file_name="edited_image.png",
                            mime="image/png"
                        )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Instructions
with st.expander("How to use this app"):
    st.markdown("""
    ### Image Editing:
    1. Upload an image
    2. Enter your edit instructions (e.g., "Add a tree in the background")
    3. Click "Process Image"
    
    ### Image Generation:
    1. Select "Generate New Image"
    2. Describe the image you want
    3. Click "Process Image"
    
    ### Tips:
    - Be specific in your prompts
    - For edits, describe exactly what changes you want
    - For generation, describe the style and content clearly
    """)

# Add API key instructions
with st.expander("Setup Instructions"):
    st.markdown("""
    ### To run this locally:
    1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)
    2. Create a `.streamlit/secrets.toml` file with:
    ```
    GEMINI_API_KEY = "your-api-key-here"
    ```
    3. Install requirements:
    ```
    pip install streamlit pillow google-generativeai
    ```
    4. Run the app:
    ```
    streamlit run app.py
    ```
    """)