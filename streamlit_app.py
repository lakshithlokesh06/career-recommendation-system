import streamlit as st

@st.cache_resource
def load_predictor():
    from predictor import recommend_career
    return recommend_career

recommend_career = load_predictor()

# ---------------- HERO SECTION ----------------
st.title("🚀 Discover Your Ideal Career Path with AI")

st.markdown("""
Find the best career based on your skills using intelligent analysis.  
Enter your skills and get personalized career recommendations instantly.

💡 Example: Python, SQL, Machine Learning, Power BI, Statistics
""")

st.markdown("")

st.button("🔍 Get Started")

st.markdown("---")

# ---------------- FEATURES SECTION ----------------
st.subheader("💡 Key Features")

st.markdown("""
✨ Smart Skill Matching  
📊 AI-Based Career Prediction  
🎯 Personalized Recommendations  
⚡ Instant Results  
""")

st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.subheader("🧠 Tell Us About Your Skills")

st.write("Select your strongest (Primary) and supporting (Secondary) skills to get accurate career recommendations.")

skill_inputs = []

for i in range(1, 6):

    st.markdown(f"### Skill {i}")

    skill = st.text_input(f"Skill {i}", key=f"skill{i}")

    type_skill = st.radio(
        "Type",
        ["Primary", "Secondary"],
        horizontal=True,
        key=f"type{i}"
    )

    skill_inputs.append((skill, type_skill))

st.markdown("")

predict = st.button("🔍 Analyze My Career Path")

# ---------------- OUTPUT SECTION ----------------
if predict:

    with st.spinner("🔍 Analyzing skills and predicting career..."):

        result = recommend_career(
            skill_inputs[0][0], skill_inputs[0][1],
            skill_inputs[1][0], skill_inputs[1][1],
            skill_inputs[2][0], skill_inputs[2][1],
            skill_inputs[3][0], skill_inputs[3][1],
            skill_inputs[4][0], skill_inputs[4][1],
        )

    st.markdown("---")
    st.subheader("🎯 Your Career Insights")

    # -------- SPLIT OUTPUT --------
    sections = result.split("Explanation:")

    main_part = sections[0]
    explanation_part = sections[1] if len(sections) > 1 else ""

    # Extract lines
    lines = main_part.split("\n")

    career = ""
    primary = ""
    secondary = ""
    other = ""
    shap_text = ""

    for line in lines:
        if "PREDICTED CAREER" in line:
            career = line.replace("PREDICTED CAREER:", "").strip()
        elif "Primary Skills Matched" in line:
            primary = line.split(":")[1].strip()
        elif "Secondary Skills Matched" in line:
            secondary = line.split(":")[1].strip()
        elif "Other Skills Entered" in line:
            other = line.split(":")[1].strip()
        elif "MODEL EXPLANATION" in line:
            shap_text += line + "\n"
        elif shap_text != "":
            shap_text += line + "\n"

    # -------- CARD 1: CAREER --------
    st.success(f"🎯 Predicted Career: {career}")

    st.markdown("")

    st.markdown(f"""
**Primary Skills:** {primary}  

**Secondary Skills:** {secondary}  

**Other Skills:** {other}
""")

    st.markdown("---")

    # -------- CARD 2: MODEL EXPLANATION --------
    st.info("📊 Model Explanation (Explainable AI)")
    st.write(shap_text)

    st.markdown("---")

    # -------- CARD 3: AI EXPLANATION --------
    st.subheader("🧠 AI Explanation")
    st.write(explanation_part)

    st.markdown("---")

    # -------- FOOTER --------
    st.caption("Built using AI & Machine Learning")
