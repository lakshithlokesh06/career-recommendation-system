import streamlit as st

@st.cache_resource
def load_predictor():
    from predictor import recommend_career
    return recommend_career

recommend_career = load_predictor()

st.title("AI Career Recommendation System")

st.write("Enter 5 skills and select whether they are Primary or Secondary.")

skill1 = st.text_input("Skill 1")
type1 = st.radio("Skill 1 Type", ["Primary","Secondary"])

skill2 = st.text_input("Skill 2")
type2 = st.radio("Skill 2 Type", ["Primary","Secondary"])

skill3 = st.text_input("Skill 3")
type3 = st.radio("Skill 3 Type", ["Primary","Secondary"])

skill4 = st.text_input("Skill 4")
type4 = st.radio("Skill 4 Type", ["Primary","Secondary"])

skill5 = st.text_input("Skill 5")
type5 = st.radio("Skill 5 Type", ["Primary","Secondary"])

if st.button("Predict Career"):

    result = recommend_career(
        skill1, type1,
        skill2, type2,
        skill3, type3,
        skill4, type4,
        skill5, type5
    )

    st.subheader("🎯 Career Recommendation")
    st.success(result)
    st.markdown("---")
