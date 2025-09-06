import streamlit as st
import requests
import os
from fpdf import FPDF

# -------------------------------
# Title
# -------------------------------
st.title("📝 AI Resume Builder")

# -------------------------------
# Form Inputs
# -------------------------------
with st.form("resume_form"):
    full_name = st.text_input("👤 Full Name")
    skills = st.text_area("💡 Skills (comma separated)")
    experience = st.text_area("💼 Work Experience")
    education = st.text_area("🎓 Education")

    submitted = st.form_submit_button("Generate Resume")

# -------------------------------
# HuggingFace API Call
# -------------------------------
if submitted:
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        st.error("❌ HuggingFace API key not found. Please set it in Streamlit secrets.")
    else:
        headers = {"Authorization": f"Bearer {api_key}"}

        prompt = f"""
        Create a professional resume for {full_name}.

        Skills: {skills}

        Work Experience: {experience}

        Education: {education}
        """

        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json={"inputs": prompt, "max_length": 500}
        )

        if response.status_code == 200:
            result = response.json()[0]['generated_text']

            st.subheader("📄 Generated Resume")
            st.write(result)

            # -------------------------------
            # PDF Export
            # -------------------------------
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, result)

            pdf_output = "resume.pdf"
            pdf.output(pdf_output)

            with open(pdf_output, "rb") as file:
                st.download_button(
                    label="⬇️ Download Resume as PDF",
                    data=file,
                    file_name="resume.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("⚠️ API request failed. Try again.")

