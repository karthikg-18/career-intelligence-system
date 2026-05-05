from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pdfplumber
import re

skills_list = [
    "python", "java", "c++", "html", "css", "javascript",
    "react", "node", "sql", "machine learning", "ai",
    "data analysis", "tkinter", "flask", "django",
    "full stack", "developer"
]

job_description = """
Looking for a Python developer with knowledge of AI, machine learning,
and experience in building applications using Tkinter or Flask.
"""

def extract_text(file):
    
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
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    return text

def skill_extract(text):
    found_skills = []
    words = text.split()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))

def match_resume_job(resume_text, job_description):
    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similarity[0][0]

def interpret_score(score):
    if score > 0.7:
        return "Excellent match"
    elif score > 0.5:
        return "Good match"
    elif score > 0.3:
        return "Average match"
    else:
        return "Low match"
    
def find_missing_skills(resume_skills, job_skills):
    missing = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)

    return missing

file_path = "Resume-Karthik.pdf" 
job_skills = skill_extract(clean_text(job_description))
resume_text = extract_text(file_path)
cleaned_text=clean_text(resume_text)
skills = skill_extract(cleaned_text)
match_score = match_resume_job(cleaned_text, job_description)

print("\n===== DETECTED SKILLS =====\n")
print(skills)
print("\n===== RESUME TEXT =====\n")
print(cleaned_text[:500])
print("\n===== MATCH SCORE =====\n")
print(round(match_score * 100, 2), "%")
missing_skills = find_missing_skills(skills, job_skills)

print("\n===== MISSING SKILLS =====\n")
print(missing_skills)
print("\n===== JOB SKILLS =====\n")
print(job_skills)
print("\n===== MATCH ANALYSIS =====\n")
print(interpret_score(match_score))
print("\n===== SUGGESTION =====\n")

if missing_skills:
    print("You should learn:", ", ".join(missing_skills))
else:
    print("Your profile matches the job well!")