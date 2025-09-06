
import streamlit as st
import os
import google.generativeai as genai
from fpdf import FPDF

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Title
st.set_page_config(page_title="Premium AI Resume Builder", layout="wide")
st.title("📝 Premium AI Resume Builder (Gemini AI)")

# -------------------------------
# Form Inputs
# -------------------------------
with st.form("resume_form"):
    full_name = st.text_input("👤 Full Name")
    phone = st.text_input("📞 Phone Number")
    email = st.text_input("✉️ Email Address")
    linkedin = st.text_input("🔗 LinkedIn URL (Optional)")
    github = st.text_input("💻 GitHub URL (Optional)")
    
    skills = st.text_area("💡 Key Skills (comma separated)")
    experience = st.text_area("💼 Work Experience (Quantifiable achievements preferred)")
    education = st.text_area("🎓 Education")
    projects = st.text_area("📂 Projects (Optional)")
    certifications = st.text_area("🏆 Certifications / Awards (Optional)")

    submitted = st.form_submit_button("Generate Premium Resume")

# -------------------------------
# Generate Resume with Gemini AI
# -------------------------------
if submitted:
    if not os.getenv("GEMINI_API_KEY"):
        st.error("❌ Gemini API key not found. Set it in Streamlit secrets.")
    else:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Generate a premium, professional, ATS-friendly resume using the information below.
Use **clean formatting, bullet points, action verbs, and concise paragraphs**.

Name: {full_name}
Phone: {phone}
Email: {email}
LinkedIn: {linkedin}
GitHub: {github}
Skills: {skills}
Experience: {experience}
Education: {education}
Projects: {projects}
Certifications: {certifications}

Structure the resume with sections:
- Header / Contact Info
- Professional Summary
- Key Skills (categorize if possible)
- Work Experience (with 2-3 quantifiable achievements per job)
- Education
- Projects (Optional)
- Certifications / Awards (Optional)
"""

        try:
            response = model.generate_content(prompt)

            if response and response.text:
                resume_text = response.text

                st.subheader("📄 Generated Premium Resume")
                st.write(resume_text)

                # -------------------------------
                # Export to PDF (Unicode + Premium)
                # -------------------------------
                pdf = FPDF()
                pdf.add_page()
                # Add Unicode font (DejaVu)
                pdf.add_font("DejaVu", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
                pdf.set_font("DejaVu", size=12)
                pdf.multi_cell(0, 10, resume_text)

                pdf_output = "premium_resume.pdf"
                pdf.output(pdf_output)

                with open(pdf_output, "rb") as file:
                    st.download_button(
                        label="⬇️ Download Resume as PDF",
                        data=file,
                        file_name="premium_resume.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("⚠️ Resume generation failed. Try again.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
