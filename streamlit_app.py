import streamlit as st

@st.cache_resource
def load_predictor():
    from predictor import recommend_career
    return recommend_career

recommend_career = load_predictor()

st.title("AI Career Recommendation System")
st.write("Enter 5 skills and select whether they are Primary or Secondary.")

skill_inputs = []

for i in range(1,6):

    skill = st.text_input(f"Skill {i}")

    type_skill = st.radio(
        f"Skill {i} Type",
        ["Primary","Secondary"],
        horizontal=True,
        key=f"type{i}"
    )

    skill_inputs.append((skill,type_skill))


predict = st.button("Predict Career")

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

    st.subheader("🎯 Career Recommendation")

    st.success(result)
