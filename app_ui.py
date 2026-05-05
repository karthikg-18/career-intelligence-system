import streamlit as st
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
st.title("Careeer Intelligence System ")
st.write("Upload your Resume and compare it with a job Description")

skills_list = [
    "python", "java", "c++", "html", "css", "javascript",
    "react", "node", "sql", "machine learning", "ai",
    "data analysis", "tkinter", "flask", "django",
    "full stack", "developer"
]

def extract_text_from_pdf(file):
    
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    return text

def skill_extract(text):
    found_skills = []
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
    return list(set(found_skills))

def match_resume_job(resume_text, job_description):
    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer(stop_words='english')  # FIX
    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similarity[0][0]

def find_missing_skills(resume_skills, job_skills):
    missing = []
    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)
    return missing

def calculate_skill_score(resume_skills, job_skills):
    if len(job_skills) == 0:
        return 0
    match_count = 0
    for skill in job_skills:
        if skill in resume_skills:
            match_count += 1
    return match_count / len(job_skills)

def interpret_score(score):
    if score > 0.7:
        return "Excellent fit"
    elif score > 0.5:
        return "Good fit"
    elif score > 0.3:
        return "Moderate fit"
    else:
        return "Needs improvement"

uploaded_file = st.file_uploader("Upload Resume (PDF)", type = ["pdf"])
job_description = st.text_area("Paste Job Description")

analyze_button = st.button("Analyze")

if analyze_button:
    if uploaded_file is not None and job_description:
        
        resume_text = extract_text_from_pdf(uploaded_file)
        cleaned_text = clean_text(resume_text)

        cleaned_job = clean_text(job_description)

        resume_skills = skill_extract(cleaned_text)
        job_skills = skill_extract(cleaned_job)
        
        tfidf_score = match_resume_job(cleaned_text, cleaned_job)
        skill_score = calculate_skill_score(resume_skills, job_skills)

        final_score = (0.7 * tfidf_score) + (0.3 * skill_score)
        missing_skills = find_missing_skills(resume_skills, job_skills)

        st.divider()
        st.subheader("📊 Analysis Results")

# Always show results
        st.metric("Match Score", f"{round(final_score * 100, 2)} %")
        st.write("**Match Analysis:**", interpret_score(final_score))

        st.write("### Match Strength")
        st.progress(final_score)

# Skills Section
        st.write("### ✅ Detected Skills")
        st.markdown(" ".join([f"`{skill}`" for skill in resume_skills]))

        st.write("### ❌ Missing Skills")
        if missing_skills:
            st.markdown(" ".join([f"`{skill}`" for skill in missing_skills]))
        else:
            st.write("No missing skills 🎉")

# Suggestions (conditional)
        if missing_skills:
            st.warning("💡 Recommended Skills to Learn:")
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.success("🎉 Your profile matches the job well!")
