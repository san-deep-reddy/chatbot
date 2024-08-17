import fitz
import streamlit as st

# Path to your picture
picture = "../files/Sandeep.jpg"

# Your name
name = "Sandeep Reddy D"
email = "reddydvvsn@gmail.com"
api_key = st.secrets["OPENAI_API_KEY"]

# URLs to your LinkedIn, GitHub, and CV
url_linkedin = "https://www.linkedin.com/in/san-deep-reddy"
url_github = "https://github.com/san-deep-reddy"
google_drive_cv_url = "https://drive.google.com/file/d/18HYq_edUMfFQyqs-0TRvAsSUOEKKg7sv/view?usp=sharing"  # Replace with actual Google Drive link

# Path to the local CV file for text extraction
local_cv_path = "../files/SandeepReddyResume.pdf"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from the resume PDF
resume_text = extract_text_from_pdf(local_cv_path)
