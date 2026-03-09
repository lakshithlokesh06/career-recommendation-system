import pandas as pd
import joblib
import streamlit as st
import requests

# Load trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Load dataset
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
        primary_list += [s.strip().lower() for s in row["primary_skills"].split(",")]
        secondary_list += [s.strip().lower() for s in row["secondary_skills"].split(",")]

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

    other_skills = [
        s for s in student_skills
        if s not in primary_list and s not in secondary_list
    ]

    prompt = f"""
A user entered the following skills: {', '.join(student_skills)}.

The predicted career path is: {predicted_career}.

Primary matched skills: {', '.join(primary_matched)}.
Secondary matched skills: {', '.join(secondary_matched)}.
Other skills entered: {', '.join(other_skills)}.

Explain in one professional paragraph why this career suits the user and how the other skills may relate to different career paths.
"""

    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {
        "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    result_json = response.json()

    if isinstance(result_json, list):
        explanation = result_json[0]["generated_text"]
    else:
        explanation = "Explanation could not be generated."

    result = f"""
PREDICTED CAREER: {predicted_career}

Primary Skills Matched:
{', '.join(primary_matched) if primary_matched else "None"}

Secondary Skills Matched:
{', '.join(secondary_matched) if secondary_matched else "None"}

Other Skills Entered:
{', '.join(other_skills) if other_skills else "None"}

Explanation:
{explanation}
"""

    return result
