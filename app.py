# ==============================================================
#  SkillMatch Backend (Flask + Pandas + Scikit-learn)
# ==============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import json
import os
import PyPDF2
from resume_parser import extract_text, extract_skills as parse_skills

# ── App setup ──
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Data storage (JSON files) ──
DATA_DIR          = "data"
USERS_FILE        = os.path.join(DATA_DIR, "users.json")
INTERNSHIPS_FILE  = os.path.join(DATA_DIR, "internships.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(file):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

users       = load_json(USERS_FILE)
internships = load_json(INTERNSHIPS_FILE)

# ── Seed sample internships if empty ──
def seed_internships():
    if len(internships) == 0:
        sample = [
            {"title": "Data Engineering Intern",  "description": "Build data pipelines",        "skills_required": "python pandas numpy sql spark postgresql"},
            {"title": "Backend Python Intern",     "description": "Build REST APIs with Flask",  "skills_required": "python flask django rest api postgresql"},
            {"title": "ML Research Intern",        "description": "NLP and ML models",           "skills_required": "python machine learning nlp scikit-learn numpy"},
            {"title": "Data Science Intern",       "description": "Analyze data and dashboards", "skills_required": "python pandas numpy matplotlib sql statistics"},
            {"title": "Full Stack Intern",         "description": "Python + React features",     "skills_required": "python flask javascript react html css"},
        ]
        internships.extend(sample)
        save_json(INTERNSHIPS_FILE, internships)
        print("Sample internships seeded!")

seed_internships()


# ──────────────────────────────────────────────
#  Helper Functions
# ──────────────────────────────────────────────

def extract_skills(text):
    """Keyword-based skill extractor for plain text input."""
    if not text:
        return []
    text = text.lower()
    skill_keywords = [
        "python", "sql", "pandas", "numpy", "flask", "django", "react",
        "docker", "ml", "machine learning", "nlp", "scikit-learn", "api",
        "tensorflow", "pytorch", "spark", "javascript", "html", "css",
        "postgresql", "mongodb", "redis", "git", "linux", "aws", "gcp",
        "statistics", "matplotlib", "jupyter", "fastapi", "rest"
    ]
    found = [s for s in skill_keywords if s in text]
    return list(set(found))


def compute_similarity(student_skills_text, internships_df):
    """
    PANDAS: loads internships into DataFrame, injects scores as new column
    NUMPY:  cosine similarity returns numpy array, np.round formats scores
    SKLEARN: TfidfVectorizer + cosine_similarity does the actual math
    """
    if internships_df.empty:
        return pd.DataFrame(columns=["title", "score", "match_pct"])

    docs = list(internships_df["skills_required"]) + [student_skills_text]

    vectorizer   = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)

    # numpy array of similarity scores
    sim = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()

    internships_df = internships_df.copy()
    internships_df["score"]     = sim
    internships_df["match_pct"] = np.round(sim * 100, 1).astype(str) + "%"

    return internships_df.sort_values("score", ascending=False)[["title", "score", "match_pct"]].head(5)


def match_internships(student_skills_text):
    df = pd.DataFrame(internships)
    if df.empty:
        return []
    ranked = compute_similarity(student_skills_text, df)
    return [
        {"title": row["title"], "score": round(float(row["score"]), 3), "match_pct": row["match_pct"]}
        for _, row in ranked.iterrows()
    ]


# ──────────────────────────────────────────────
#  ROUTES
# ──────────────────────────────────────────────

@app.route("/")
def home():
    return jsonify({
        "status" : "running",
        "message": "SkillMatch API is live",
        "routes" : [
            "POST /api/register",
            "POST /api/login",
            "POST /api/upload-resume",
            "POST /api/match",
            "GET  /api/internships",
            "POST /api/internships",
            "GET  /api/students",
            "GET  /api/analytics"
        ]
    })


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not {"name", "email", "role"}.issubset(data):
        return jsonify({"error": "Missing fields: name, email, role"}), 400
    if any(u["email"] == data["email"] for u in users):
        return jsonify({"error": "User already exists"}), 400
    user = {"name": data["name"], "email": data["email"], "role": data["role"], "skills": []}
    users.append(user)
    save_json(USERS_FILE, users)
    return jsonify({"message": "Registered successfully", "user": user})


@app.route("/api/login", methods=["POST"])
def login():
    data  = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email required"}), 400
    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "Login successful", "user": user})


@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    """
    PyPDF2 reads the uploaded PDF.
    resume_parser.extract_skills() uses re (regex) to find skills.
    Skills are saved to the user's record and returned as JSON.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # PyPDF2 reads, regex extracts
    raw_text = extract_text(filepath)
    skills   = parse_skills(raw_text)

    # Save skills to matching user
    email = request.form.get("email", "")
    for u in users:
        if u["email"] == email:
            u["skills"] = skills
            save_json(USERS_FILE, users)
            break

    return jsonify({
        "success"    : True,
        "skills"     : skills,
        "skill_count": len(skills),
        "message"    : f"{len(skills)} skills extracted from your resume!"
    })


@app.route("/api/match", methods=["POST"])
def match():
    """
    Accepts { "student_skills": ["python", "pandas"] } or a plain string.
    Returns internships ranked by cosine similarity score.
    """
    data = request.get_json()
    if not data or "student_skills" not in data:
        return jsonify({"error": "Missing student_skills"}), 400

    student_text = " ".join(data["student_skills"]) if isinstance(data["student_skills"], list) else str(data["student_skills"])
    found_skills = extract_skills(student_text)
    matches      = match_internships(" ".join(found_skills))

    return jsonify({"input_skills": found_skills, "match_count": len(matches), "matches": matches})


@app.route("/api/internships", methods=["GET"])
def get_internships():
    return jsonify({"count": len(internships), "internships": internships})


@app.route("/api/internships", methods=["POST"])
def post_internship():
    data = request.get_json()
    if not data or not {"title", "description", "skills_required"}.issubset(data):
        return jsonify({"error": "Missing: title, description, skills_required"}), 400
    internship = {"title": data["title"], "description": data["description"], "skills_required": data["skills_required"]}
    internships.append(internship)
    save_json(INTERNSHIPS_FILE, internships)
    return jsonify({"message": "Internship posted!", "internship": internship}), 201


@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify({"count": len(users), "students": users})


@app.route("/api/analytics", methods=["GET"])
def analytics():
    """
    pandas: explodes skill strings into rows, counts frequency
    numpy:  computes average skills per internship
    """
    df = pd.DataFrame(internships)
    if df.empty:
        return jsonify({"total_internships": 0, "top_skills": {}})

    skill_counts = (
        df["skills_required"]
          .str.split()
          .explode()
          .str.lower()
          .value_counts()
          .head(10)
          .to_dict()
    )
    avg_skills = float(np.mean(df["skills_required"].str.split().apply(len)))

    return jsonify({
        "total_internships"        : len(internships),
        "total_students"           : len(users),
        "avg_skills_per_internship": round(avg_skills, 1),
        "top_skills"               : skill_counts
    })


# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("SkillMatch API — http://localhost:5000")
    app.run(debug=True)