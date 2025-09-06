import streamlit as st
import requests
from fpdf import FPDF
import os

# HuggingFace API
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
headers = {"Authorization": f"Bearer " + API_KEY}

def generate_resume_summary(text):
    payload = {"inputs": f"Write a professional resume summary for: {text}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()[0]["generated_text"]
    except Exception as e:
        return "Error generating summary. Please check API key or model."

# Streamlit UI
st.title("AI Resume Builder ✨")

name = st.text_input("Full Name")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Work Experience")
education = st.text_area("Education")

if st.button("Generate Resume"):
    user_input = f"Name: {name}\nSkills: {skills}\nExperience: {experience}\nEducation: {education}"
    summary = generate_resume_summary(user_input)

    st.subheader("AI Generated Resume Summary")
    st.write(summary)

    # PDF Export
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Resume for {name}\n\nSummary:\n{summary}\n\nSkills:\n{skills}\n\nExperience:\n{experience}\n\nEducation:\n{education}")
    pdf.output("resume.pdf")

    with open("resume.pdf", "rb") as f:
        st.download_button("⬇️ Download Resume (PDF)", f, file_name="resume.pdf")
