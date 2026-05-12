from similarity import calculate_similarity


resume = """
Experienced Python developer with machine learning skills
"""


job_description = """
Looking for ML engineer with Python experience
"""


score = calculate_similarity(resume, job_description)

print(score)