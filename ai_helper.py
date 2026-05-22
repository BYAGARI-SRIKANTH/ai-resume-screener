from google import genai

# Add your Gemini API key
API_KEY = "AIzaSyBJclWWnEORgMHlOcoaemMUmbI8IliluiM"

client = genai.Client(api_key=API_KEY)


def generate_ai_feedback(resume_text, job_description):

    prompt = f"""
    You are an AI hiring assistant.

    Compare this resume with job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give:
    1. Resume summary
    2. Strengths
    3. Weaknesses
    4. Suggested improvements
    5. 5 interview questions

    Keep response short and professional.
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"AI Error: {str(e)}"