def check_evidence(text_category, image_category):

    matches = {
        "Roads": "Pothole",
        "Sanitation": "Garbage"
    }

    if text_category in matches:

        if image_category == matches[text_category]:
            return "Verified"

        elif image_category == "Normal":
            return "Needs Verification"

        else:
            return "Needs Verification"

    return "Image Verification Not Applicable"