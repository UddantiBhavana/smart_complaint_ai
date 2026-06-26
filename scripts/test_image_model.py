import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.image_classifier.predictor import predict_image

img_path = input("Enter image path: ")

category, confidence = predict_image(img_path)

print("\nPrediction Result")
print("------------------")
print("Category :", category)
print(f"Confidence : {confidence:.2f}%")