# 🚀 Career Intelligence System

An AI-powered web application that analyzes resumes and compares them with job descriptions to provide match scores, skill gaps, and improvement suggestions.

---

## 📌 Features

- 📄 Resume parsing (PDF)
- 🧠 NLP-based similarity using TF-IDF
- 🎯 Match score calculation
- 🧩 Skill extraction & comparison
- ⚠️ Missing skills detection
- 💡 Skill improvement suggestions
- 📊 Interactive UI using Streamlit

---

## 🛠️ Tech Stack

- Python
- Streamlit
- pdfplumber
- scikit-learn (TF-IDF, Cosine Similarity)

---

## 📊 How it Works

1. Upload your resume (PDF)
2. Paste a job description
3. System:
   - Extracts text from resume
   - Cleans text
   - Matches with job description
   - Calculates similarity score
   - Suggests missing skills

---

## 📸 Demo

(Add screenshot here)

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
python -m streamlit run app_ui.py

# 🚀 STEP 2: Save + Push to GitHub

In terminal run:

```bash
git add README.md
git commit -m "Added README"
git push