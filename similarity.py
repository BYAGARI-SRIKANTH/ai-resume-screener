from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity


# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_similarity(resume_text, job_description):

    # Convert text into embeddings
    resume_embedding = model.encode([resume_text])

    jd_embedding = model.encode([job_description])

    # Compare similarity
    similarity_score = cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    # Convert to percentage
    return round(similarity_score * 100, 2)