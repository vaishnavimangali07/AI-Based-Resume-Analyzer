import streamlit as st
import base64
import re
import os
import webbrowser
from pypdf import PdfReader

# -------------------------------
# Utility Functions
# -------------------------------

def extract_resume_text(file_path: str) -> str:
    """Extract text from PDF resume."""
    reader = PdfReader(file_path)
    return " ".join([page.extract_text() or "" for page in reader.pages])


def parse_resume(text: str) -> dict:
    """Extract structured info from resume text."""
    resume_data = {}

    lines = text.split("\n")

    # Name
    for line in lines:
        line_clean = line.strip()
        if line_clean and len(line_clean.split()) <= 5 and line_clean[0].isupper():
            resume_data["Name"] = line_clean
            break

    # Email
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if match:
        resume_data["Email"] = match.group(0)

    # Phone
    match = re.search(r"\+?\d[\d\s-]{8,}\d", text)
    if match:
        resume_data["Phone"] = match.group(0).strip()

    # Skills
    possible_skills = ["Python", "Java", "C++", "SQL", "Machine Learning",
                       "Excel", "Data Analysis", "HTML", "CSS", "JavaScript"]

    found_skills = [skill.lower() for skill in possible_skills if skill.lower() in text.lower()]
    resume_data["Skills"] = found_skills

    # Education
    edu_keywords = ["btech", "b.tech", "bachelor", "computer science",
                    "engineering", "msc", "mtech", "master"]

    found_edu = [word for word in edu_keywords if word in text.lower()]
    resume_data["Education"] = ", ".join(found_edu) if found_edu else "Not found"

    return resume_data


def analyze_skills(resume_skills: list, job_skills: list):
    """Compare resume skills with job skills."""
    
    # Convert everything to lowercase (FIX 🔥)
    resume_skills = [s.lower() for s in resume_skills]
    job_skills = [s.lower() for s in job_skills]

    matched = []
    for skill in job_skills:
        if skill in resume_skills:
            matched.append(skill)

    missing = [skill for skill in job_skills if skill not in matched]

    score = (len(matched) / len(job_skills)) * 100 if job_skills else 0

    return matched, missing, score


def display_pdf(file_path: str):
    """Show PDF inside app."""
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" 
    width="100%" height="500"></iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)


def open_pdf_in_browser(file_path: str):
    """Open PDF in browser."""
    abs_path = os.path.abspath(file_path)
    webbrowser.open(f"file:///{abs_path}")


# -------------------------------
# Streamlit App
# -------------------------------

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# ✅ Safe Font (no UI break)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">

<style>
body, p, h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
}
</style>
""", unsafe_allow_html=True)


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


if uploaded_file is not None and job_input:

    # Save file
    with open("resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Resume uploaded successfully!")

    # Extract text
    resume_text = extract_resume_text("resume.pdf")

    # Parse
    resume_data = parse_resume(resume_text)

    # Job skills input clean
    job_skills = [skill.strip().lower() for skill in job_input.split(",") if skill.strip()]

    # Analyze
    matched_skills, missing_skills, score = analyze_skills(
        resume_data.get("Skills", []), job_skills
    )

    # Resume Preview
    st.subheader("📄 Resume Preview")
    display_pdf("resume.pdf")

    # Results
    st.subheader("📊 Analysis Result")

    st.success(f"✅ Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}")
    st.error(f"❌ Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}")

    st.write(f"🎯 Resume Score: {score:.2f}%")
    st.progress(int(score))
    if missing_skills:
        st.info(f"🤖 AI Suggestion: Consider adding {', '.join(missing_skills)} to improve your resume.")
    import matplotlib.pyplot as plt

    labels = ["Matched Skills", "Missing Skills"]
    sizes = [len(matched_skills), len(missing_skills)]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')

    st.subheader("🥧 Skill Analysis Pie Chart")
    st.pyplot(fig)

    # Feedback
    if score > 80:
        st.success("Excellent match! 🎉")
    elif score > 50:
        st.info("Good match 👍 but can improve")
    else:
        st.warning("Needs improvement ⚠️")


    st.markdown("---")

    import graphviz

    st.subheader("🔄 Application Flowchart")

    flow = graphviz.Digraph()
    flow.node("A", "Start")
    flow.node("B", "Upload Resume")
    flow.node("C", "Extract Text from PDF")
    flow.node("D", "Parse Resume Data")
    flow.node("E", "Enter Job Skills")
    flow.node("F", "Analyze Skills")
    flow.node("G", "Calculate Score")
    flow.node("H", "Show Results & Suggestions")
    flow.node("I", "Download Report")
    flow.node("J", "End")

    flow.edges([
        ("A","B"),
        ("B","C"),
        ("C","D"),
        ("D","E"),
        ("E","F"),
        ("F","G"),
        ("G","H"),
        ("H","I"),
        ("I","J")
  
   ])

    st.graphviz_chart(flow)

    # Resume summary
    st.subheader("📑 Resume Summary")

    for key, value in resume_data.items():
        if isinstance(value, list):
            value = ", ".join(value)
        st.write(f"{key}: {value}")
            # Open in browser
    if st.button("Open Resume in Browser"):
        open_pdf_in_browser("resume.pdf")

        # ✅ Download Report (FINAL FIXED)
    report = f"""
Resume Analysis Report

Matched Skills: {', '.join(matched_skills)}
Missing Skills: {', '.join(missing_skills)}
Score: {score:.2f}%
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_report.txt",
        mime="text/plain"
    )