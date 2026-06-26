import re
import joblib

model = joblib.load("models/complaint_classifier.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

replacements = {
    "streetlights": "street light",
    "streetlight": "street light",

    "potholes": "pothole",

    "garbages": "dirty",
    "garbage": "dirty",
    "trash": "dirty",
    "waste": "dirty",
    "rubbish": "dirty",

    "drainage": "sewer",
    "drains": "sewer",
    "drain": "sewer",

    "roads": "street",
    "road": "street",

    "taps": "water",
    "tap": "water",
    "pipeline": "water",

    "speed breakers": "speed breaker",
    "speed bumps": "speed bump",
    "garbages": "garbage",
    "pipes": "pipe",
    "leaks": "leak",
    "streetlights": "street light"
}

def rule_based_category(text):

    text = text.lower()

    # Drainage
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
    
    # Water
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

    # Electricity
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

    # Sanitation
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

    # Roads
    
    if any(word in text for word in [
        "road",
        "street",
        "pothole",
        "speed breaker",
        "speed bump",
        "road hump",
        "footpath",
        "sidewalk",
        "bridge",
        "crack",
        "cracked road",
        "damaged road",
        "broken road",
        "road repair",
        "road damage",
        "uneven road"
    ]):
        return "Roads"

    return None

def predict_category(text):

    original_text = text.lower()

    prediction = rule_based_category(original_text)

    if prediction is not None:
        return prediction

    processed_text = original_text

    for old_word, new_word in replacements.items():

        processed_text = re.sub(
            rf"\b{re.escape(old_word)}\b",
            new_word,
            processed_text
        )

    vector = vectorizer.transform([processed_text])

    prediction = model.predict(vector)[0]

    return prediction