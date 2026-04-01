import streamlit as st

@st.cache_resource
def load_predictor():
    from predictor import recommend_career
    return recommend_career

recommend_career = load_predictor()

# ---------------- HEADER ----------------
st.title("🚀 AI Career Recommendation System")
st.write("Find your ideal career path using AI-driven skill analysis.")

st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.subheader("🧠 Enter Your Skills")

skill_inputs = []

for i in range(1, 6):

    st.markdown(f"### Skill {i}")

    skill = st.text_input(f"Skill {i}", key=f"skill{i}")

    type_skill = st.radio(
        f"Type",
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

    sections = result.split("Explanation:")

    main_output = sections[0]
    explanation_output = sections[1] if len(sections) > 1 else ""

    # Career + XAI
    st.success(main_output)

    st.markdown("")

    # AI Explanation
    st.info("🧠 AI Explanation")
    st.write(explanation_output)

    st.markdown("---")

    st.caption("Built using AI & Machine Learning")
