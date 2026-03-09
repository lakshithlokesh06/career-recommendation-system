import pandas as pd
import requests
import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

data = pd.read_csv("career_dataset.csv")

def recommend_career(skill1, type1, skill2, type2, skill3, type3, skill4, type4, skill5, type5):

    skills = []

    if type1 == "Primary":
        skills.extend([skill1, skill1])
    else:
        skills.append(skill1)

    if type2 == "Primary":
        skills.extend([skill2, skill2])
    else:
        skills.append(skill2)

    if type3 == "Primary":
        skills.extend([skill3, skill3])
    else:
        skills.append(skill3)

    if type4 == "Primary":
        skills.extend([skill4, skill4])
    else:
        skills.append(skill4)

    if type5 == "Primary":
        skills.extend([skill5, skill5])
    else:
        skills.append(skill5)

    skills_text = " ".join(skills)
    vector = vectorizer.transform([skills_text])

    predicted_career = model.predict(vector)[0]

    career_rows = data[data["career_path"] == predicted_career]

    primary_list = []
    secondary_list = []

    for _, row in career_rows.iterrows():
        primary_list += [s.strip() for s in row["primary_skills"].lower().split(",")]
        secondary_list += [s.strip() for s in row["secondary_skills"].lower().split(",")]

    primary_list = list(set(primary_list))
    secondary_list = list(set(secondary_list))

    student_skills = [
        skill1.lower().strip(),
        skill2.lower().strip(),
        skill3.lower().strip(),
        skill4.lower().strip(),
        skill5.lower().strip()
    ]

    primary_matched = [s for s in student_skills if s in primary_list]
    secondary_matched = [s for s in student_skills if s in secondary_list]

    url = "http://localhost:11434/api/generate"

    prompt = f"""
Explain why {predicted_career} is suitable for someone with primary skills
{', '.join(primary_matched)} and secondary skills {', '.join(secondary_matched)}.
Also explain why learning the remaining required skills will help in this career.
Write one professional paragraph.
"""

    explanation = requests.post(
        url,
        json={"model": "llama3:8b", "prompt": prompt, "stream": False}
    ).json()["response"]

    result = f"""
PREDICTED CAREER: {predicted_career}

Primary Skills Matched:
{', '.join(primary_matched)}

Secondary Skills Matched:
{', '.join(secondary_matched)}

Explanation:
{explanation}
"""

    return result

