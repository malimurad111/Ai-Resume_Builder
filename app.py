import streamlit as st
import os
from fpdf import FPDF
import google.generativeai as genai

# -------------------------------
# Configure Gemini AI
# -------------------------------
if not os.getenv("GEMINI_API_KEY"):
    st.warning("⚠️ Set your Gemini API Key in Streamlit secrets to enable AI resume generation.")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Entry-Level AI Resume Builder", layout="wide")
st.title("📝 Entry-Level AI Resume Builder (Gemini AI)")

st.markdown(
    """
Welcome! Fill in your details below and generate a **premium, ATS-friendly resume** instantly.
Your resume will be professionally formatted and downloadable as a PDF.
"""
)

# -------------------------------
# Resume Form Inputs
# -------------------------------
with st.form("resume_form"):
    full_name = st.text_input("👤 Full Name", "Ali Shahbaz")
    phone = st.text_input("📞 Phone Number", "03034055548")
    email = st.text_input("✉️ Email Address", "m.alishahbaz01@gmail.com")
    linkedin = st.text_input("🔗 LinkedIn URL", "https://linkedin.com/in/alishahbaz")
    github = st.text_input("💻 GitHub URL", "https://github.com/alishahbaz")
    
    skills = st.text_area(
        "💡 Key Skills (comma separated)",
        "Python, Java, C++, JavaScript, SQL, Git, Agile methodologies"
    )
    experience = st.text_area(
        "💼 Work Experience / Internships (Quantifiable achievements)",
        "XYZ Corp – Software Engineering Intern: Improved process efficiency by 15%. Collaborated with 4 developers to deliver a project on time and within budget."
    )
    education = st.text_area(
        "🎓 Education",
        "BBIT, University Name, City – May 2024 | GPA: 3.6 | Relevant Coursework: Data Structures, Database Management, Software Engineering Principles, Web Development"
    )
    projects = st.text_area(
        "📂 Projects (Optional)",
        "Project Name – GitHub Link: Brief description, technologies used, key achievements, quantifiable results."
    )
    certifications = st.text_area(
        "🏆 Certifications / Awards (Optional)",
        "Certification Name, Issuing Organization, Date (Optional)"
    )

    submitted = st.form_submit_button("Generate Premium Resume")

# -------------------------------
# Generate Resume with Gemini AI
# -------------------------------
if submitted:
    if not os.getenv("GEMINI_API_KEY"):
        st.error("❌ Gemini API key not found. Please set it in Streamlit secrets.")
    else:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
Generate a **premium, professional, entry-level, ATS-friendly resume** using the information below.
- Replace placeholders with realistic examples if left empty.
- Use bold headings, bullet points, action verbs, and concise paragraphs.
- Tailored for recent graduates or entry-level positions.

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

Structure the resume as:
- Header / Contact Info
- Professional Summary
- Key Skills
- Work Experience
- Education
- Projects (Optional)
- Certifications / Awards (Optional)
"""

            response = model.generate_content(prompt)
            resume_text = response.text if response and response.text else None

            if resume_text:
                st.subheader("📄 Generated Premium Entry-Level Resume")
                st.text_area("Preview", resume_text, height=400)

                # -------------------------------
                # Export to PDF
                # -------------------------------
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("DejaVu", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
                pdf.set_font("DejaVu", size=12)
                pdf.multi_cell(0, 10, resume_text)
                
                pdf_output = "premium_entry_level_resume.pdf"
                pdf.output(pdf_output)

                with open(pdf_output, "rb") as file:
                    st.download_button(
                        label="⬇️ Download Resume as PDF",
                        data=file,
                        file_name="premium_entry_level_resume.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("⚠️ Resume generation failed. Please try again or check your input.")

        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
