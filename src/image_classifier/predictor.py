import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Load trained model
model = tf.keras.models.load_model(
    "models/image_classifier.keras"
)

# Class names
CLASS_NAMES = [
    "Garbage",
    "Normal",
    "Pothole"
]


def predict_image(img_path):
    """
    Predict category of an image.

    Parameters:
        img_path (str): Path of image

    Returns:
        category (str)
        confidence (float)
    """

    img = image.load_img(
        img_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    prediction = model.predict(
        img_array,
        verbose=0
    )

    class_index = np.argmax(prediction)

    confidence = np.max(prediction) * 100

    category = CLASS_NAMES[class_index]

    return category, confidence


if __name__ == "__main__":

    img_path = input(
        "Enter image path: "
    )

    category, confidence = predict_image(
        img_path
    )

    print("\nPrediction Result")
    print("------------------")
    print("Category :", category)
    print(
        f"Confidence : {confidence:.2f}%"
    )