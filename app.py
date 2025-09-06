import streamlit as st
import os
import google.generativeai as genai
from fpdf import FPDF

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Title
st.title("📝 AI Resume Builder (Powered by Gemini AI)")

# Form
with st.form("resume_form"):
    full_name = st.text_input("👤 Full Name")
    skills = st.text_area("💡 Skills (comma separated)")
    experience = st.text_area("💼 Work Experience")
    education = st.text_area("🎓 Education")

    submitted = st.form_submit_button("Generate Resume")

# Generate Resume
if submitted:
    if not os.getenv("GEMINI_API_KEY"):
        st.error("❌ Gemini API key not found. Please set it in Streamlit secrets.")
    else:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        Write a professional and ATS-friendly resume for {full_name}.
        Use this structure:

        Name:
        Summary:
        Skills:
        Work Experience:
        Education:

        Details:
        - Skills: {skills}
        - Work Experience: {experience}
        - Education: {education}
        """

        response = model.generate_content(prompt)

        if response and response.text:
            resume_text = response.text

            st.subheader("📄 Generated Resume")
            st.write(resume_text)

            # Export to PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, resume_text)

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
            st.error("⚠️ Resume generation failed. Try again.")
