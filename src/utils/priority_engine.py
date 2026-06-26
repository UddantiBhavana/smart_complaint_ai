def calculate_priority(complaint_text):

    text = complaint_text.lower()

    high_keywords = [
        "accident",
        "danger",
        "injury",
        "fire",
        "outage",
        "collapsed"
    ]

    medium_keywords = [
        "leak",
        "overflow",
        "garbage",
        "pothole"
    ]

    score = 50

    for word in high_keywords:
        if word in text:
            score += 30

    for word in medium_keywords:
        if word in text:
            score += 15

    score = min(score, 100)

    if score >= 80:
        severity = "High"
    elif score >= 60:
        severity = "Medium"
    else:
        severity = "Low"

    return severity, score