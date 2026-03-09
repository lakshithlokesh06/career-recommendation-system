import pandas as pd
import joblib

data = pd.read_csv("career_dataset.csv")

print(data.head())

data["skills"] = data["skill1"] + " " + data["skill2"] + " " + data["skill3"] + " " + data["skill4"] + " " + data["skill5"]

print(data[["skills","career_path"]].head())

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(data["skills"])
y = data["career_path"]

print(X.shape)
print(y.head())

from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()

model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model training completed")

test_skills = ["python machine learning statistics"]

test_vector = vectorizer.transform(test_skills)

prediction = model.predict(test_vector)

print("Predicted Career:", prediction[0])

