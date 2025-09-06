import streamlit as st
import os
import google.generativeai as genai
from fpdf import FPDF

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Premium Entry-Level AI Resume Builder", layout="wide")
st.title("📝 Premium Entry-Level AI Resume Builder (Gemini AI)")

# -------------------------------
# Form Inputs
# -------------------------------
with st.form("resume_form"):
    full_name = st.text_input("👤 Full Name", "Ali Shahbaz")
    phone = st.text_input("📞 Phone Number", "03034055548")
    email = st.text_input("✉️ Email Address", "m.alishahbaz01@gmail.com")
    linkedin = st.text_input("🔗 LinkedIn URL", "https://linkedin.com/in/alishahbaz")
    github = st.text_input("💻 GitHub URL", "https://github.com/alishahbaz")
    
    skills = st.text_area("💡 Key Skills (comma separated)", "Python, Java, C++, JavaScript, Git, SQL, Agile methodologies")
    experience = st.text_area(
        "💼 Work Experience (Quantifiable achievements / Internships)", 
        "Internship at XYZ Corp: Improved process efficiency by 15%. Collaborated with team to deliver project on time."
    )
    education = st.text_area(
        "🎓 Education", 
        "BBIT, University Name, City – 2024 | GPA: 3.6 | Relevant Coursework: Data Structures, Database Management, Software Engineering"
    )
    projects = st.text_area(
        "📂 Projects (Optional)", 
        "Project Name: Brief description, technologies used, key achievements. Include GitHub links if available."
    )
    certifications = st.text_area(
        "🏆 Certifications / Awards (Optional)", 
        "Certification Name, Issuing Organization, Date"
    )

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
Generate a **premium, professional, entry-level ATS-friendly resume** using the information below.
- Replace any placeholders with realistic examples if left empty.
- Use bold headings, bullet points, action verbs, and concise paragraphs.
- Tailor for recent graduates or entry-level positions.

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

        try:
            response = model.generate_content(prompt)

            if response and response.text:
                resume_text = response.text

                st.subheader("📄 Generated Premium Entry-Level Resume")
                st.write(resume_text)

                # -------------------------------
                # Export to PDF (Unicode + Premium)
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
                st.error("⚠️ Resume generation failed. Try again.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
