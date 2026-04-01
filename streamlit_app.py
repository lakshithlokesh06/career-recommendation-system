import streamlit as st

@st.cache_resource
def load_predictor():
    from predictor import recommend_career
    return recommend_career

recommend_career = load_predictor()

# -------- SESSION STATE --------
if "started" not in st.session_state:
    st.session_state.started = False

# -------- BACKGROUND STYLE --------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1f2937, #020617);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
if not st.session_state.started:

    st.markdown("""
    <h1 style='text-align: center;'>🚀 Discover Your Ideal Career Path with AI</h1>

    <p style='text-align: center; font-size:18px;'>
    Find the best career based on your skills using intelligent analysis.<br>
    Enter your skills and get personalized career recommendations instantly.
    </p>

    <p style='text-align: center; font-size:16px;'>
    💡 Example: Python, SQL, Machine Learning, Power BI, Statistics
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- FIXED CENTER BUTTON --------
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("""
        <style>
        div.stButton > button {
            width: 100%;
            padding: 14px;
            font-size: 18px;
            border-radius: 12px;
            border: 1px solid #444;
            background-color: #111827;
            color: white;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background-color: #1f2937;
            border: 1px solid #666;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("🔍 Get Started"):
            st.session_state.started = True
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #333;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- FEATURES ----------------
    st.markdown("<h2 style='text-align: center;'>💡 Key Features</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✨ Smart Skill Matching")
        st.markdown("Accurately matches your skills with career paths.")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### 🎯 Personalized Recommendations")
        st.markdown("Gives tailored career suggestions based on your input.")

    with col2:
        st.markdown("### 📊 AI-Based Prediction")
        st.markdown("Uses intelligent models for accurate predictions.")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### ⚡ Instant Results")
        st.markdown("Get career insights instantly.")

# ---------------- INPUT + OUTPUT ----------------
else:

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

        main_part = sections[0]
        explanation_part = sections[1] if len(sections) > 1 else ""

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
                continue
            elif shap_text != "" or "prediction of" in line.lower():
                shap_text += line + "\n"

        # -------- CARD 1 --------
        st.success(f"🎯 Predicted Career: {career}")

        st.markdown(f"""
**Primary Skills:** {primary}  

**Secondary Skills:** {secondary}  

**Other Skills:** {other}
""")

        st.markdown("---")

        # -------- CARD 2 --------
        st.info("📊 Model Explanation (Explainable AI)")
        st.write(shap_text.strip())

        st.markdown("---")

        # -------- CARD 3 --------
        st.subheader("🧠 AI Explanation")
        st.write(explanation_part)

        st.markdown("---")
        st.caption("Built using AI & Machine Learning")
