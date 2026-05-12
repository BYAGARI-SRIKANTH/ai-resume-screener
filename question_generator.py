def generate_questions(skills):

    questions = []

    if "python" in skills:
        questions.append(
            "Explain list vs tuple in Python."
        )

        questions.append(
            "What are Python decorators?"
        )

    if "machine learning" in skills:
        questions.append(
            "What is overfitting?"
        )

        questions.append(
            "Difference between supervised and unsupervised learning?"
        )

    if "sql" in skills:
        questions.append(
            "What is JOIN in SQL?"
        )

    if len(questions) == 0:
        questions.append(
            "Tell me about yourself."
        )

    return questions