import re


# Skill Database
SKILLS_DB = [

    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "data analysis",
    "communication",
    "flask",
    "django",
    "pandas",
    "numpy",
    "power bi",
    "excel",
    "tableau",
    "aws",
    "docker",
    "deployment",
    "api",
    "java",
    "javascript",
    "react"
]


# Clean Text
def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    return text


# Extract Skills
def extract_skills(text):

    found_skills = []

    for skill in SKILLS_DB:

        if skill.lower() in text:

            found_skills.append(skill)

    return list(set(found_skills))


# Extract Email
def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return "Not Found"


# Extract Phone
def extract_phone(text):

    pattern = r"(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}"

    phones = re.findall(pattern, text)

    if phones:

        numbers = re.findall(r"\d+", "".join(phones[0]))

        return "".join(numbers)

    return "Not Found"


# Improvement Suggestions
def generate_suggestions(missing_skills):

    suggestions = []

    for skill in missing_skills:

        suggestions.append(
            f"Add experience or projects related to {skill}"
        )

    if len(missing_skills) == 0:

        suggestions.append(
            "Strong profile for this role"
        )

    return suggestions