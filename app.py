from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import google.generativeai as genai
import pdf2image


poppler_path = r"C:\Users\Anusha Tomar\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
        first_page = images[0]
        
    
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")



st.set_page_config(page_title="JobFit Analyzer")

st.markdown(
    """
    <style>
    body {
        color: white;
        background-color: black;
    }
    .stApp {
        background-color: black;
    }
    .st-bb {
        background-color: black;
    }
    .st-at {
        background-color: #333333;
    }
    .st-c0 {
        background-color: black;
    }
    .st-bw {
        color: white;
    }
    .st-cr {
        color: white;
    }
    .stTextInput>div>div>input {
        color: white;
    }
    .stTextArea textarea {
        color: white;
        background-color: #333333;
    }
    .stButton>button {
        color: white;
        background-color: #333333;
        border: 1px solid #555555;
    }
    .stButton>button:hover {
        background-color: #555555;
    }
    .uploadedFile {
        color: white;
    }
    .css-145kmo2 {
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    /* Make all text white */
    .stMarkdown, .stText, label, .stTextArea label, .stFileUploader label {
        color: white !important;
        text-decoration:italic;
    }
    /* Ensure file uploader text is white */
    .stFileUploader div[data-testid="stFileUploaderDropzone"] {
        color: white !important;
        text-decoration:italic;
    }
    /* Make placeholder text visible */
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("JobFit Analyzer - An AI tool to help you match your resume with your dream job ⭐")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First, the output should come as a percentage and then keywords missing and lastly final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")