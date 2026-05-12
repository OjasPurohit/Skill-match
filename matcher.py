import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match(student_skills, internships):
    # Safety checks
    if not isinstance(student_skills, list):
        raise ValueError("student_skills must be a list")

    if len(student_skills) == 0:
        raise ValueError("student_skills is empty")

    if 'skills' not in internships.columns:
        raise KeyError("Column 'skills' not found in internships DataFrame")

    internships = internships.copy()

    # Clean data
    docs = internships['skills'].fillna("").astype(str).tolist()
    docs.append(" ".join(student_skills))

    # TF-IDF
    tfidf = TfidfVectorizer().fit_transform(docs)

    # Similarity
    sim = cosine_similarity(tfidf[-1], tfidf[:-1])[0]

    # Scores
    internships['match_score'] = sim * 100
    internships['match_pct'] = internships['match_score'].round(2).astype(str) + "%"

    return internships.sort_values(by="match_score", ascending=False)