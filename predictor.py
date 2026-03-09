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

    # -------- AI PROMPT --------

    prompt = f"""
You are an AI career advisor.

A student entered the following skills:
{', '.join(student_skills)}

The predicted career is: {predicted_career}

Primary matched skills: {', '.join(primary_matched)}
Secondary matched skills: {', '.join(secondary_matched)}
Other skills: {', '.join(other_skills)}

Write three short paragraphs:

Paragraph 1:
Explain why the PRIMARY skills ({', '.join(primary_matched)}) strongly match the career {predicted_career}.

Paragraph 2:
Explain how the SECONDARY skills ({', '.join(secondary_matched)}) support this career.
Also suggest which career paths commonly use these skills.

Paragraph 3:
Explain how the OTHER skills ({', '.join(other_skills)}) relate to different career paths.
Suggest possible careers where these skills are useful.

Leave one blank line between each paragraph.
"""

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    headers = {
        "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 220,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        result_json = response.json()

        if isinstance(result_json, list) and "generated_text" in result_json[0]:
            explanation = result_json[0]["generated_text"]
        else:
            explanation = f"{predicted_career} is recommended because the provided skills align with the requirements of this role."

    except Exception:
        explanation = f"{predicted_career} is recommended because the provided skills align with the requirements of this role."

    result = f"""
PREDICTED CAREER: {predicted_career}

Primary Skills Matched: {', '.join(primary_matched) if primary_matched else "None"}

Secondary Skills Matched: {', '.join(secondary_matched) if secondary_matched else "None"}

Other Skills Entered: {', '.join(other_skills) if other_skills else "None"}

Explanation:

{explanation}
"""

    return result
