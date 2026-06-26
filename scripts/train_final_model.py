import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

print("Loading dataset...")

df = pd.read_csv(
    "datasets/complaints/processed/complaints_balanced.csv"
)

X = df["complaint_text"]
y = df["category"]

print("Creating TF-IDF vectors...")

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english"
)

X_tfidf = vectorizer.fit_transform(X)

print("Training Linear SVM...")

model = LinearSVC()

model.fit(X_tfidf, y)

print("Saving model...")

joblib.dump(
    model,
    "models/complaint_classifier.pkl"
)

joblib.dump(
    vectorizer,
    "models/vectorizer.pkl"
)

print("Done!")
print("Model saved to models/")