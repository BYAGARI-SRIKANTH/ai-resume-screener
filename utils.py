import re

SKILLS = [
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


def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    return text


def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def extract_email(text):

    match = re.search(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+",
        text
    )

    if match:
        return match.group(0)

    return "Not Found"


def extract_phone(text):

    match = re.search(
        r"\+?\d[\d -]{8,12}\d",
        text
    )

    if match:
        return match.group(0)

    return "Not Found"