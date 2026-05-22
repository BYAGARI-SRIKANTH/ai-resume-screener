import os
import csv
import pdfplumber

from flask import Flask, render_template, request
from docx import Document

from utils import (
    clean_text,
    extract_skills,
    extract_email,
    extract_phone,
    generate_suggestions
)

from similarity import calculate_similarity


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Read Resume File
def read_resume(file_path):

    text = ""

    # PDF
    if file_path.endswith(".pdf"):

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

    # DOCX
    elif file_path.endswith(".docx"):

        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    # TXT
    elif file_path.endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

    return text


@app.route("/", methods=["GET", "POST"])

def home():

    results = []
    jd_skills = []

    if request.method == "POST":

        uploaded_files = request.files.getlist("resume")

        job_description = request.form["job_description"]

        cleaned_jd = clean_text(job_description)

        jd_skills = extract_skills(cleaned_jd)

        for uploaded_file in uploaded_files:

            if uploaded_file:

                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    uploaded_file.filename
                )

                uploaded_file.save(file_path)

                # Read resume
                text = read_resume(file_path)

                cleaned_resume = clean_text(text)

                # Resume skills
                resume_skills = extract_skills(cleaned_resume)

                # AI Score
                score = calculate_similarity(
                    cleaned_resume,
                    cleaned_jd
                )

                # Matched Skills
                matched_skills = []

                for skill in resume_skills:

                    if skill in jd_skills:
                        matched_skills.append(skill)

                # Missing Skills
                missing_skills = []

                for skill in jd_skills:

                    if skill not in resume_skills:
                        missing_skills.append(skill)

                # Suggestions
                suggestions = generate_suggestions(
                    missing_skills
                )

                # Email + Phone
                email = extract_email(text)

                phone = extract_phone(text)

                # Recommendation
                if score >= 75:
                    recommendation = "Excellent Match"

                elif score >= 50:
                    recommendation = "Good Match"

                else:
                    recommendation = "Average Match"

                # Store results
                results.append({

                    "filename": uploaded_file.filename,

                    "email": email,

                    "phone": phone,

                    "score": score,

                    "matched": matched_skills,

                    "missing": missing_skills,

                    "suggestions": suggestions,

                    "recommendation": recommendation
                })

        # Sort ranking
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # Save CSV
        with open(
            "candidate_rankings.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Resume",
                "Email",
                "Phone",
                "AI Score",
                "Matched Skills",
                "Missing Skills"
            ])

            for candidate in results:

                writer.writerow([
                    candidate["filename"],
                    candidate["email"],
                    candidate["phone"],
                    candidate["score"],
                    ", ".join(candidate["matched"]),
                    ", ".join(candidate["missing"])
                ])

    return render_template(
        "index.html",
        results=results,
        jd_skills=jd_skills
    )


if __name__ == "__main__":

    app.run(debug=True)