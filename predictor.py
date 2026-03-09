import pandas as pd
import joblib
import streamlit as st
from groq import Groq

# Load trained model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Load dataset
data = pd.read_csv("career_dataset.csv")

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


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

    primary_matched = list(set([s for s in student_skills if s in primary_list]))
    secondary_matched = list(set([s for s in student_skills if s in secondary_list]))

    other_skills = [
        s for s in student_skills
        if s not in primary_list and s not in secondary_list
    ]

    prompt = f"""
You are an AI career advisor.

Student skills: {', '.join(student_skills)}

Predicted career: {predicted_career}

Primary skills: {', '.join(primary_matched)}
Secondary skills: {', '.join(secondary_matched)}
Other skills: {', '.join(other_skills)}

Write exactly three paragraphs.

Paragraph 1: Explain why the primary skills match the career.

Paragraph 2: Explain how secondary skills support this career and mention related careers.

Paragraph 3: Explain how other skills relate to other possible career paths.

Leave one blank line between paragraphs.
"""

    chat = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert career advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        top_p=1,
        max_tokens=400,
        stream=False
    )

    explanation = chat.choices[0].message.content

    result = f"""
PREDICTED CAREER: {predicted_career}

Primary Skills Matched: {', '.join(primary_matched) if primary_matched else "None"}

Secondary Skills Matched: {', '.join(secondary_matched) if secondary_matched else "None"}

Other Skills Entered: {', '.join(other_skills) if other_skills else "None"}

Explanation:

{explanation}
"""

    return result
