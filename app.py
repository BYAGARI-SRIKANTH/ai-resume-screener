import csv
import os
import pdfplumber

from flask import (
    Flask,
    render_template,
    request,
    send_file
)

from utils import (
    clean_text,
    extract_skills,
    extract_email,
    extract_phone
)

from similarity import calculate_similarity
from question_generator import generate_questions

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Default skills
MASTER_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "communication",
    "flask",
    "django",
    "tensorflow",
    "pandas",
    "numpy"
]


@app.route("/", methods=["GET", "POST"])
def home():

    results = []

    detected_jd_skills = []

    if request.method == "POST":

        job_description = request.form["job_description"]

        uploaded_files = request.files.getlist("resume")

        cleaned_jd = clean_text(job_description)

        jd_skills = extract_skills(cleaned_jd)

        detected_jd_skills = jd_skills

        for uploaded_file in uploaded_files:

            if uploaded_file:

                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    uploaded_file.filename
                )

                uploaded_file.save(file_path)

                # Extract PDF text
                text = ""

                with pdfplumber.open(file_path) as pdf:

                    for page in pdf.pages:

                        extracted = page.extract_text()

                        if extracted:
                            text += extracted

                # Clean text
                cleaned_resume = clean_text(text)

                # Extract skills
                resume_skills = extract_skills(cleaned_resume)

                # Matched skills
                matched_skills = []

                for skill in resume_skills:

                    if skill in jd_skills:
                        matched_skills.append(skill)

                # Missing skills
                missing_skills = []

                for skill in jd_skills:

                    if skill not in resume_skills:
                        missing_skills.append(skill)

                # AI similarity
                score = calculate_similarity(
                    cleaned_resume,
                    cleaned_jd
                )

                # Recommendation
                if score >= 75:
                    recommendation = "Excellent Match"

                elif score >= 50:
                    recommendation = "Good Match"

                else:
                    recommendation = "Needs Improvement"

                # AI feedback
                if len(missing_skills) == 0:
                    feedback = "Candidate matches all required skills."

                else:
                    feedback = (
                        "Candidate matches most required skills "
                        "but has some missing areas."
                    )

                # Interview questions
                questions = generate_questions(matched_skills)

                # Contact extraction
                email = extract_email(text)
                phone = extract_phone(text)

                # Add result
                results.append({

                    "filename": uploaded_file.filename,

                    "score": score,

                    "matched": matched_skills,

                    "missing": missing_skills,

                    "recommendation": recommendation,

                    "feedback": feedback,

                    "questions": questions,

                    "email": email,

                    "phone": phone
                })

        # Sort by score
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
                "Rank",
                "Resume",
                "Score",
                "Recommendation",
                "Email",
                "Phone"
            ])

            for index, candidate in enumerate(results, start=1):

                writer.writerow([
                    index,
                    candidate["filename"],
                    candidate["score"],
                    candidate["recommendation"],
                    candidate["email"],
                    candidate["phone"]
                ])

    return render_template(
        "index.html",
        results=results,
        total_resumes=len(results),
        detected_jd_skills=detected_jd_skills
    )


@app.route("/download")
def download_file():

    return send_file(
        "candidate_rankings.csv",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)