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

/* Feature Cards */
.feature-box {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px;
    transition: 0.3s;
    backdrop-filter: blur(10px);
    height: 100%;
}

.feature-box:hover {
    transform: translateY(-5px);
    border: 1px solid #4f46e5;
    box-shadow: 0 8px 25px rgba(79,70,229,0.3);
}

.feature-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}

.feature-desc {
    font-size: 14px;
    color: #cbd5f5;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
if not st.session_state.started:

    st.markdown("""
    <h1 style='text-align: center;
               font-size: 52px;
               font-weight: 800;
               background: linear-gradient(90deg, #4f46e5, #22c55e, #06b6d4);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;'>
    AI Career Recommendation System
    </h1>

    <h2 style='text-align: center;
               font-size: 32px;
               font-weight: 600;
               color:#cbd5f5;'>
    🚀 Discover Your Ideal Career Path with AI
    </h2>

    <p style='text-align: center; font-size:18px;'>
    Find the best career based on your skills using intelligent analysis.<br>
    Enter your skills and get personalized career recommendations instantly.
    </p>

    <p style='text-align: center; font-size:16px;'>
    💡 Example: Python, SQL, Machine Learning, Power BI, Statistics
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- CENTER BUTTON --------
    col1, col2, col3 = st.columns([2,1.5,2])

    with col2:
        if st.button("➜ Get Started"):
            st.session_state.started = True
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------- FEATURES --------
    st.markdown("<h2 style='text-align:center;'>⚙️ What Makes This System Powerful</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">🧠 Smart Skill Analysis</div>
            <div class="feature-desc">
            Weighs primary and secondary skills intelligently for better prediction.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">⚙️ ML Prediction Engine</div>
            <div class="feature-desc">
            Uses trained ML model to identify the most suitable career path.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">📊 Explainable AI</div>
            <div class="feature-desc">
            Shows how each skill impacts the prediction (High, Medium, Low).
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">🤖 LLM Explanation</div>
            <div class="feature-desc">
            Generates human-like explanations using Groq-powered AI.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">⚡ Instant Insights</div>
            <div class="feature-desc">
            Get results instantly with detailed insights.
            </div>
        </div>
        """, unsafe_allow_html=True)

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

        st.success(f"Predicted Career: {career}")

        st.markdown(f"""
**Primary Skills:** {primary}  

**Secondary Skills:** {secondary}  

**Other Skills:** {other}
""")

        st.markdown("---")

        st.info("📊 Model Explanation (Explainable AI)")
        st.write(shap_text.strip())

        st.markdown("---")

        st.subheader("🧠 AI Explanation")
        st.write(explanation_part)

        st.markdown("---")
        st.caption("Built using AI & Machine Learning")
