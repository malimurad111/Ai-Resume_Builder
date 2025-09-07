import streamlit as st
import os
from fpdf import FPDF
import google.generativeai as genai
from docx import Document

# ------------------ Gemini API ------------------
if not os.getenv("GEMINI_API_KEY"):
    st.warning("⚠️ Set your Gemini API Key in Streamlit secrets.")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Entry-Level AI Resume Builder", layout="wide")
st.title("📝 Entry-Level AI Resume Builder (Gemini AI)")

st.markdown("Fill your details below and generate a **premium, ATS-friendly resume** in PDF or Word!")

# ------------------ Form ------------------
with st.form("resume_form"):
    full_name = st.text_input("👤 Full Name", "Ali Shahbaz")
    phone = st.text_input("📞 Phone Number", "03034055548")
    email = st.text_input("✉️ Email Address", "m.alishahbaz01@gmail.com")
    linkedin = st.text_input("🔗 LinkedIn URL", "https://linkedin.com/in/alishahbaz")
    github = st.text_input("💻 GitHub URL", "https://github.com/alishahbaz")
    skills = st.text_area("💡 Key Skills (comma separated)", "Python, Java, C++, JavaScript, SQL, Git, Agile methodologies")
    experience = st.text_area("💼 Work Experience / Internships", "XYZ Corp – Software Engineering Intern: Improved process efficiency by 15%.")
    education = st.text_area("🎓 Education", "BBIT, University Name, City – May 2024 | GPA: 3.6")
    projects = st.text_area("📂 Projects (Optional)", "Project Name – GitHub Link: Brief description, technologies used.")
    certifications = st.text_area("🏆 Certifications / Awards (Optional)", "Certification Name, Issuing Organization, Date")
    submitted = st.form_submit_button("Generate Premium Resume")

# ------------------ Generate Resume ------------------
if submitted:
    if not os.getenv("GEMINI_API_KEY"):
        st.error("❌ Gemini API key not found.")
    else:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
Generate a **premium, professional, entry-level, ATS-friendly resume** using the information below.
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
Structure: Header, Professional Summary, Key Skills, Work Experience, Education, Projects, Certifications.
"""
            response = model.generate_content(prompt)
            resume_text = response.text if response and response.text else None

            if resume_text:
                st.subheader("📄 Generated Premium Entry-Level Resume")
                st.text_area("Preview", resume_text, height=400)

                # ------------------ PDF Export ------------------
                pdf = FPDF()
                pdf.add_page()

                # Absolute path for DejaVuSans.ttf
                font_path = os.path.join(os.getcwd(), "assets", "fonts", "DejaVuSans.ttf")
                pdf.add_font("DejaVu", "", fname=font_path, uni=True)
                pdf.set_font("DejaVu", size=12)
                pdf.multi_cell(0, 10, resume_text)

                pdf_output = "premium_entry_level_resume.pdf"
                pdf.output(pdf_output)

                with open(pdf_output, "rb") as file:
                    st.download_button(
                        "⬇️ Download Resume as PDF",
                        file,
                        file_name="premium_entry_level_resume.pdf",
                        mime="application/pdf"
                    )

                # ------------------ Word Export ------------------
                doc = Document()
                for line in resume_text.split("\n"):
                    doc.add_paragraph(line)
                word_output = "premium_entry_level_resume.docx"
                doc.save(word_output)

                with open(word_output, "rb") as file:
                    st.download_button(
                        "⬇️ Download Resume as Word (.docx)",
                        file,
                        file_name="premium_entry_level_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            else:
                st.error("⚠️ Resume generation failed. Try again.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
