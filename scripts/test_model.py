import re
import joblib

# Load model and vectorizer
model = joblib.load("models/complaint_classifier.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

# Department Mapping
departments = {
    "Roads": "Road Maintenance Department",
    "Water": "Water Supply Department",
    "Electricity": "Electrical Department",
    "Drainage": "Drainage Department",
    "Sanitation": "Sanitation Department"
}

# Resolution Recommendations
recommendations = {
    "Roads": "Inspect road condition and dispatch repair team.",
    "Water": "Inspect water pipeline and restore supply.",
    "Electricity": "Send electrical maintenance crew to inspect the issue.",
    "Drainage": "Inspect sewer network and clear blockage.",
    "Sanitation": "Schedule waste collection and sanitation team."
}

# Word normalization dictionary
replacements = {

    # Electricity
    "electricity": "street light",
    "power": "street light",
    "current": "street light",
    "outage": "street light",
    "blackout": "street light",
    "cutoff": "street light",
    "cut off": "street light",

    # Street lights
    "streetlights": "street light",
    "streetlight": "street light",
    "light pole": "lamppost",

    # Roads
    "potholes": "pothole",
    "roads": "street",
    "road": "street",

    # Water
    "taps": "water",
    "tap": "water",
    "water pipe": "water",
    "pipeline": "water",

    # Drainage
    "drainage": "sewer",
    "drains": "sewer",
    "drain": "sewer",

    # Sanitation
    "garbages": "dirty",
    "garbage": "dirty",
    "trash": "dirty",
    "waste": "dirty",
    "rubbish": "dirty"
}

print("=" * 60)
print("AI Smart Civic Complaint Classifier")
print("=" * 60)
print("Categories:", list(model.classes_))
print("Type 'exit' to quit.")

def rule_based_category(text):

    text = text.lower()

    if any(word in text for word in [
    "electricity",
    "power",
    "current",
    "outage",
    "blackout",
    "cutoff",
    "cut off"]):
        return "Electricity"

    if any(word in text for word in
           ["water", "tap", "pipeline"]):
        return "Water"

    if any(word in text for word in
           ["garbage", "trash", "waste", "rubbish"]):
        return "Sanitation"

    if any(word in text for word in
           ["drain", "drainage", "sewer"]):
        return "Drainage"

    if any(word in text for word in
           ["road", "street", "pothole"]):
        return "Roads"

    return None

while True:

    complaint = input("\nEnter Complaint: ").strip()

    if complaint.lower() == "exit":
        print("\nExiting...")
        break

    # Keep original text for rule checking
    original_complaint = complaint.lower()

    # -------------------------------
    # Rule Based Classification First
    # -------------------------------

    prediction = rule_based_category(original_complaint)

    # -------------------------------
    # If rule not matched, use ML model
    # -------------------------------

    if prediction is None:

        processed_complaint = original_complaint

        for old_word, new_word in replacements.items():

            processed_complaint = re.sub(
                rf"\b{re.escape(old_word)}\b",
                new_word,
                processed_complaint
            )

        print("\nProcessed Text:")
        print(processed_complaint)

        vector = vectorizer.transform(
            [processed_complaint]
        )

        prediction = model.predict(
            vector
        )[0]

        scores = None

        if hasattr(model, "decision_function"):
            scores = model.decision_function(vector)[0]

    else:

        print("\nRule-Based Classification Used")
        print("Processed Text:")
        print(original_complaint)

        scores = None

    department = departments.get(
        prediction,
        "General Administration"
    )

    recommendation = recommendations.get(
        prediction,
        "No recommendation available."
    )

    print("\nPrediction Results")
    print("-" * 30)
    print("Category      :", prediction)
    print("Department    :", department)
    print("Recommendation:", recommendation)

    if scores is not None:

        print("\nCategory Scores")
        print("-" * 30)

        for category, score in zip(
            model.classes_,
            scores
        ):
            print(f"{category:<12}: {score:.4f}")