# ==============================================================
#  SkillMatch Backend (Flask + Pandas + Scikit-learn)
# ==============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS   # ✅ ADDED
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import json
import os

# ✅ FIRST create app
app = Flask(__name__)

# ✅ ENABLE CORS (VERY IMPORTANT)
CORS(app)

# ✅ HOME ROUTE
@app.route('/')
def home():
    return "Backend is running successfully 🚀"

# --------------------------------------------------------------
# Data storage
# --------------------------------------------------------------
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
INTERNSHIPS_FILE = os.path.join(DATA_DIR, "internships.json")

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

users = load_json(USERS_FILE)
internships = load_json(INTERNSHIPS_FILE)

# --------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------

def extract_skills(text):
    if not text:
        return []

    text = text.lower()
    skill_keywords = [
        "python", "sql", "pandas", "numpy", "flask", "django", "react",
        "docker", "ml", "machine learning", "nlp", "scikit-learn", "api",
        "tensorflow", "pytorch", "spark", "javascript", "html", "css"
    ]

    found = [skill for skill in skill_keywords if skill in text]
    return list(set(found))


def compute_similarity(student_skills, internships_df):
    if internships_df.empty:
        return pd.DataFrame(columns=['title', 'score'])

    docs = list(internships_df["skills_required"]) + [student_skills]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)

    sim = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
    internships_df["score"] = sim
    ranked = internships_df.sort_values(by="score", ascending=False)
    return ranked[["title", "score"]].head(5)


def match_internships(student_skills_text):
    internships_df = pd.DataFrame(internships)
    if internships_df.empty:
        return []

    ranked = compute_similarity(student_skills_text, internships_df)
    results = [
        {"title": row["title"], "score": round(float(row["score"]), 3)}
        for _, row in ranked.iterrows()
    ]
    return results

# --------------------------------------------------------------
# API ROUTES
# --------------------------------------------------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    required = {"name", "email", "role"}
    if not data or not required.issubset(data):
        return jsonify({"error": "Missing fields"}), 400

    if any(u["email"] == data["email"] for u in users):
        return jsonify({"error": "User already exists"}), 400

    user = {
        "name": data["name"],
        "email": data["email"],
        "role": data["role"]
    }
    users.append(user)
    save_json(USERS_FILE, users)
    return jsonify({"message": "User registered successfully", "user": user})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email required"}), 400

    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "Login successful", "user": user})


@app.route("/api/internships", methods=["POST"])
def post_internship():
    data = request.get_json()
    required = {"title", "description", "skills_required"}
    if not data or not required.issubset(data):
        return jsonify({"error": "Missing fields"}), 400

    internship = {
        "title": data["title"],
        "description": data["description"],
        "skills_required": data["skills_required"]
    }

    internships.append(internship)
    save_json(INTERNSHIPS_FILE, internships)
    return jsonify({"message": "Internship posted", "internship": internship})


@app.route("/api/internships", methods=["GET"])
def get_internships():
    return jsonify({"internships": internships})


@app.route("/api/match", methods=["POST"])
def match():
    data = request.get_json()
    if not data or "student_skills" not in data:
        return jsonify({"error": "Missing student_skills"}), 400

    if isinstance(data["student_skills"], list):
        student_text = " ".join(data["student_skills"])
    else:
        student_text = str(data["student_skills"])

    found_skills = extract_skills(student_text)
    matches = match_internships(" ".join(found_skills))

    return jsonify({
        "input_skills": found_skills,
        "matches": matches
    })

# --------------------------------------------------------------
# Run app
# --------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)