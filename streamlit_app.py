import streamlit as st

@st.cache_resource
def load_predictor():
    from predictor import recommend_career
    return recommend_career

recommend_career = load_predictor()

st.title("AI Career Recommendation System")

st.write("Enter 5 skills and select whether they are Primary or Secondary.")

# Create two columns
col1, col2 = st.columns([2,1])

with col1:

    skill1 = st.text_input("Skill 1")
    type1 = st.radio("Skill 1 Type", ["Primary","Secondary"], horizontal=True)

    skill2 = st.text_input("Skill 2")
    type2 = st.radio("Skill 2 Type", ["Primary","Secondary"], horizontal=True)

    skill3 = st.text_input("Skill 3")
    type3 = st.radio("Skill 3 Type", ["Primary","Secondary"], horizontal=True)

    skill4 = st.text_input("Skill 4")
    type4 = st.radio("Skill 4 Type", ["Primary","Secondary"], horizontal=True)

    skill5 = st.text_input("Skill 5")
    type5 = st.radio("Skill 5 Type", ["Primary","Secondary"], horizontal=True)

predict = st.button("Predict Career")

if predict:

    with st.spinner("🔍 Analyzing skills and predicting career..."):

        result = recommend_career(
            skill1, type1,
            skill2, type2,
            skill3, type3,
            skill4, type4,
            skill5, type5
        )

    with col2:
        st.subheader("🎯 Career Recommendation")
        st.success(result)
        st.markdown("---")
