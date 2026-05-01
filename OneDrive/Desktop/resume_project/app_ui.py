
import streamlit as st
from PyPDF2 import PdfReader

# Page config
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# ✅ CSS
st.markdown("""
<style>
body {
    background-color: #F8F9FA;
}
.main {
    background-color: #F8F9FA;
}
h1 {
    color: #6C63FF;
    text-align: center;
}
.card {
    padding: 15px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("📄 AI-Based Resume Analyzer")
st.markdown("---")

# Sidebar
st.sidebar.header("📌 Instructions")
st.sidebar.write("""
1. Upload your resume (PDF)
2. Enter job skills
3. View analysis results
""")

# Upload + Input
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_input = st.text_input("Enter Job Skills (comma separated)")

if uploaded_file and job_input:
    st.success("✅ Resume uploaded successfully!")

    # Extract text directly from uploaded file
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    resume_text = resume_text.lower()

    # Skills
    job_skills = [skill.strip().lower() for skill in job_input.split(",")]
    matched_skills = [skill for skill in job_skills if skill in resume_text]
    missing_skills = [skill for skill in job_skills if skill not in matched_skills]

    score = (len(matched_skills) / len(job_skills)) * 100

    # Results
    st.subheader("📊 Analysis Result")
    st.write("✅ Matched Skills:", matched_skills)
    st.write("❌ Missing Skills:", missing_skills)
    st.write(f"🎯 Resume Score: {score:.2f}%")

    st.progress(int(score))

    if score > 80:
        st.success("Excellent match! 🎉")
    elif score > 50:
        st.info("Good match 👍 but can improve")
    else:
        st.warning("Needs improvement ⚠️")

    st.markdown("---")

    # ✅ Resume Preview (inside the block so resume_text exists)
    st.subheader("📃 Extracted Resume Text (Preview)")
    st.write(resume_text[:500])

# Sidebar bottom
st.sidebar.title("Options")
st.sidebar.write("Upload resume and enter skills")