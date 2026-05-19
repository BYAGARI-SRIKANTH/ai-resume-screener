from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def calculate_similarity(
    resume_text,
    job_description
):

    resume_embedding = get_model().encode(...)

    jd_embedding = model.encode(
        [job_description]
    )

    similarity_score = cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    return round(
        similarity_score * 100,
        2
    )