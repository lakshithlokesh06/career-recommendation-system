import pandas as pd
import joblib
import streamlit as st
from openai import OpenAI

# Load trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Load dataset
data = pd.read_csv("career_dataset.csv")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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
You are an AI career advisor.

A student has entered the following skills:
{', '.join(student_skills)}

Predicted career: {predicted_career}

Primary matched skills: {', '.join(primary_matched)}
Secondary matched skills: {', '.join(secondary_matched)}
Other skills: {', '.join(other_skills)}

Write EXACTLY THREE paragraphs.

Paragraph 1 - PRIMARY SKILLS:
Explain how the primary skills help in the career {predicted_career}.

Paragraph 2 - SECONDARY SKILLS:
Explain how the secondary skills support this career and mention careers where these skills are useful.

Paragraph 3 - OTHER SKILLS:
Explain how the other skills relate to different career paths and suggest possible careers where these skills are useful.

Each paragraph should contain 3–4 sentences.
Leave one blank line between paragraphs.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an AI career advisor."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=300
)

explanation = response.choices[0].message.content

    result = f"""
PREDICTED CAREER: {predicted_career}

Primary Skills Matched: {', '.join(primary_matched) if primary_matched else "None"}

Secondary Skills Matched: {', '.join(secondary_matched) if secondary_matched else "None"}

Other Skills Entered: {', '.join(other_skills) if other_skills else "None"}

Explanation:

{explanation}
"""

    return result
