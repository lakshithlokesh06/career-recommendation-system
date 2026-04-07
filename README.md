# AI-Based Career Recommendation System

An intelligent web application that recommends suitable career paths based on user-provided skills using Machine Learning, Explainable AI, and LLM-powered insights.

---

## Overview

Choosing the right career path can be overwhelming. This system simplifies the process by analyzing user skills and predicting the most relevant career options.

It not only provides predictions but also explains *why* a particular career is recommended, improving trust and transparency.

---

## Features

* 🔍 **Skill-Based Prediction**
  Input 5 skills and get personalized career recommendations.

* **Machine Learning Model**
  Processes and classifies skills into primary and secondary categories for accurate predictions.

*  **Explainable AI (XAI)**
  SHAP-inspired approach highlights how each skill impacts the prediction:

  * High Impact
  * Moderate Impact
  * Low Impact

  **LLM Integration (Groq API)**
  Generates detailed, human-readable explanations for recommendations.

* **Interactive UI (Streamlit)**
  Clean and user-friendly interface with:

  * Landing page
  * Structured input form
  * Organized output display

---

## System Architecture

1. **User Input Layer**

   * Collects 5 skills from the user

2. **Skill Processing Module**

   * Classifies skills as primary or secondary

3. **Prediction Engine**

   * Machine learning model predicts career path

4. **Orchestrator Layer (`predictor.py`)**

   * Manages end-to-end workflow:

     * Input processing
     * Prediction
     * Output generation

5. **Explainability Module**

   * Calculates feature importance (SHAP-inspired)

6. **LLM Explanation Layer**

   * Uses Groq API to generate detailed explanations

7. **Frontend (Streamlit)**

   * Displays predictions and insights

---

## Tech Stack

* **Programming Language:** Python
* **Machine Learning:** Scikit-learn (or your model library)
* **Explainable AI:** SHAP-inspired logic
* **LLM API:** Groq
* **Frontend:** Streamlit

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/career-recommendation-system.git

# Navigate to project folder
cd career-recommendation-system

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## Example Input

```text
Skills:
- Python
- Machine Learning
- Data Analysis
- Communication
- Problem Solving
```

### Output:

* Recommended Career: Data Scientist

* Skill Impact:

  * Python → High
  * Machine Learning → High
  * Communication → Moderate

* AI-Generated Explanation:

  > "Based on your strong technical and analytical skills..."

---

## Future Improvements

* Feedback loop for continuous learning
* Multiple career predictions with confidence scores
* Integration with real-world datasets (LinkedIn, O*NET)
* Career roadmap suggestions (skills + courses)
* Cloud deployment (AWS / Streamlit Cloud)

---

## Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📬 Contact

If you have any questions or suggestions, feel free to reach out!

---

⭐ If you like this project, don't forget to star the repository!
