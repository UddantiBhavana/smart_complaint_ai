import re
import joblib

# Load trained model and vectorizer
model = joblib.load("models/complaint_classifier.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


# --------------------------------------------------
# Text replacements
# --------------------------------------------------
replacements = {

    # Electricity
    "streetlights": "street light",
    "streetlight": "street light",

    # Roads
    "roads": "street",
    "road": "street",
    "potholes": "pothole",
    "speed breakers": "speed breaker",
    "speed bumps": "speed bump",

    # Sanitation
    "garbages": "garbage",
    "garbage": "dirty",
    "trash": "dirty",
    "waste": "dirty",
    "rubbish": "dirty",

    # Drainage
    "drainage": "sewer",
    "drains": "sewer",
    "drain": "sewer",

    # Water
    "taps": "water",
    "tap": "water",
    "pipeline": "water",
    "pipes": "pipe",
    "leaks": "leak"
}


# --------------------------------------------------
# Rule-Based Classification
# --------------------------------------------------
def rule_based_category(text):

    text = text.lower()

    # ==========================================
    # High Priority Keywords
    # ==========================================

    if "pothole" in text:
        return "Roads"

    if "street light" in text or "streetlight" in text:
        return "Electricity"

    if "garbage" in text or "trash" in text or "waste" in text:
        return "Sanitation"

    if "water supply" in text or "pipeline" in text or "burst pipe" in text:
        return "Water"

    if "drainage" in text or "sewer" in text:
        return "Drainage"

    # ==========================================
    # Drainage
    # ==========================================

    if any(word in text for word in [
        "drain",
        "drainage",
        "sewer",
        "sewage",
        "overflow",
        "waterlogging",
        "blocked drain",
        "manhole",
        "drain pipe"
    ]):
        return "Drainage"

    # ==========================================
    # Roads  (Moved BEFORE Water)
    # ==========================================

    if any(word in text for word in [
        "road",
        "street",
        "pothole",
        "damaged road",
        "broken road",
        "road repair",
        "road damage",
        "road crack",
        "crack",
        "crater",
        "uneven road",
        "speed breaker",
        "speed bump",
        "road hump",
        "footpath",
        "sidewalk",
        "bridge",
        "asphalt"
    ]):
        return "Roads"

    # ==========================================
    # Electricity
    # ==========================================

    if any(word in text for word in [
        "electricity",
        "power",
        "current",
        "street light",
        "streetlight",
        "lamppost",
        "transformer",
        "wire",
        "electric pole",
        "power cut",
        "power outage",
        "blackout",
        "voltage",
        "fuse"
    ]):
        return "Electricity"

    # ==========================================
    # Sanitation
    # ==========================================

    if any(word in text for word in [
        "garbage",
        "trash",
        "waste",
        "dirty",
        "rubbish",
        "dustbin",
        "cleaning",
        "overflowing bin",
        "litter",
        "unclean"
    ]):
        return "Sanitation"

    # ==========================================
    # Water
    # ==========================================

    if any(word in text for word in [
        "water",
        "water supply",
        "tap",
        "taps",
        "pipeline",
        "pipe",
        "leak",
        "leaking",
        "burst pipe",
        "drinking water",
        "low pressure",
        "dirty water"
    ]):
        return "Water"

    return None


# --------------------------------------------------
# Prediction Function
# --------------------------------------------------
def predict_category(text):

    original_text = text.lower()

    # Rule-based prediction first
    prediction = rule_based_category(original_text)

    if prediction is not None:
        return prediction

    # Text preprocessing
    processed_text = original_text

    for old_word, new_word in replacements.items():

        processed_text = re.sub(
            rf"\b{re.escape(old_word)}\b",
            new_word,
            processed_text
        )

    # ML Prediction
    vector = vectorizer.transform([processed_text])

    prediction = model.predict(vector)[0]

    return prediction