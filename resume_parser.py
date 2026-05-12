import PyPDF2
import re

SKILLS_DB = [
    "python", "java", "sql", "machine learning",
    "data analysis", "html", "css", "javascript"
]

def extract_text(path):
    text = ""
    try:
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:   # avoid None error
                    text += page_text

    except Exception as e:
        print("Error reading PDF:", e)

    return text.lower()


def extract_skills(text):
    found = []

    for skill in SKILLS_DB:
        # Escape special characters + handle multi-word skills
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)

    return list(set(found))