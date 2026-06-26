from src.complaint_classifier.classifier import predict_category
from src.routing.department_router import get_department
from src.recommender.recommendation_engine import get_recommendation
from src.image_classifier.predictor import predict_image
from src.validation.evidence_checker import check_evidence
from src.database.db_manager import (
    create_database,
    insert_complaint
)

# Create database if not exists
create_database()

complaint = input("Enter Complaint: ")

image_path = input(
    "Enter Image Path (leave blank if none): "
)

category = predict_category(
    complaint
)

department = get_department(
    category
)

recommendation = get_recommendation(
    category
)

print("\n===== TEXT ANALYSIS =====")
print("Category:", category)
print("Department:", department)
print("Recommendation:", recommendation)

# Default values
image_category = "Not Provided"
confidence = 0.0

if image_path.strip():

    image_category, confidence = predict_image(
        image_path
    )

    print("\n===== IMAGE ANALYSIS =====")
    print("Image Category:", image_category)
    print(
        f"Confidence: {confidence:.2f}%"
    )

status = check_evidence(
    category,
    image_category
)

print("\nEvidence Status:", status)

# Save complaint into database
insert_complaint(
    complaint_text=complaint,
    text_category=category,
    image_category=image_category,
    confidence=confidence,
    evidence_status=status,
    department=department,
    recommendation=recommendation
)