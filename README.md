# 🚀 AI-Powered Smart Civic Complaint Resolution & Prediction System

## 📌 Overview

The **AI-Powered Smart Civic Complaint Resolution & Prediction System** is an intelligent web application that automates the process of reporting, classifying, routing, tracking, and resolving civic complaints using Artificial Intelligence. The system leverages **Natural Language Processing (NLP)** and **Computer Vision** to improve complaint management, reduce manual effort, and ensure efficient service delivery.

This project was developed as part of the **Edunet Foundation – IBM SkillsBuild – AICTE AI Internship**.

---

## ✨ Key Features

### 👤 Citizen Module
- Submit civic complaints through a user-friendly interface.
- AI-based complaint category prediction.
- Automatic department assignment.
- Priority score calculation based on complaint severity.
- Image verification for Roads and Sanitation complaints.
- Duplicate complaint detection.
- Track complaint status.
- Complaint reopening request.
- Feedback submission after resolution.

---

### 👮 Department Officer Module
- Secure department officer login.
- Department-wise complaint dashboard.
- Update complaint status.
- Upload completion images.
- AI verification of completion images.
- View complaint activity timeline.
- Complaint resolution management.

---

### 👑 Admin Module
- Overall complaint monitoring.
- Complaint analytics dashboard.
- Department-wise performance analysis.
- Complaint history management.

---

### 🏢 Supported Departments

The system automatically routes complaints to the appropriate department based on the predicted complaint category.

- 🛣️ Road Maintenance Department
- 🗑️ Sanitation Department
- 💧 Water Supply Department
- ⚡ Electricity Department
- 🌧️ Drainage Department

---

## 🧠 AI Features

- Complaint Classification using Machine Learning
- Automatic Department Routing
- Image Verification using CNN
- Duplicate Complaint Detection
- Priority Prediction
- Evidence Verification
- Complaint Tracking
- Analytics Dashboard

---

## 🛠️ Technologies Used

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- Python
- SQLite Database

### Machine Learning & AI
- Scikit-learn
- TensorFlow
- Logistic Regression
- TF-IDF Vectorizer
- Convolutional Neural Network (CNN)

### Python Libraries
- Pandas
- NumPy
- OpenCV
- Pillow
- Matplotlib
- Plotly
- Joblib

---

## 🤖 AI Models Used

### Text Classification
- TF-IDF Vectorizer
- Logistic Regression Classifier

### Image Classification

CNN model trained to classify images into:

- Garbage
- Pothole
- Normal

### Duplicate Detection

- Cosine Similarity
- Address Similarity Matching

---

## 📂 Project Structure

```text
smart_complaint_ai/
│
├── models/
│   ├── complaint_classifier.pkl
│   ├── image_classifier.keras
│   └── vectorizer.pkl
│
├── notebooks/
├── output/
├── scripts/
│
├── src/
│   ├── complaint_classifier/
│   ├── database/
│   ├── image_classifier/
│   ├── recommender/
│   ├── routing/
│   ├── utils/
│   └── validation/
│
├── app.py
├── app_test.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ System Workflow

1. Citizen submits a complaint.
2. AI analyzes the complaint text.
3. Complaint category is predicted.
4. Complaint is routed to the appropriate department.
5. Priority score is calculated.
6. Image verification is performed (Roads & Sanitation).
7. Duplicate complaints are detected.
8. Complaint is stored in the database.
9. Department officer updates complaint status.
10. Citizen tracks complaint progress and submits feedback.

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart_complaint_ai.git
```

### Move into the project folder

```bash
cd smart_complaint_ai
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
streamlit run app.py
```

---

## 📊 Future Enhancements

- Mobile application (Android & iOS)
- GIS-based complaint location mapping
- SMS & Email notifications
- WhatsApp chatbot integration
- Multilingual complaint support
- Cloud deployment using AWS or Azure
- Advanced AI analytics for Smart City management

---

## Demo Login Credentials

### Admin

Username: admin

Password: admin123

### Department Officers

| Department | Username | Password |
|------------|----------|----------|
| Road Maintenance | road_officer | road123 |
| Sanitation | sanitation_officer | clean123 |
| Water Supply | water_officer | water123 |
| Electricity | electric_officer | elec123 |
| Drainage | drainage_officer | drain123 |

---

## 📚 Dataset

The original datasets are **not included** in this repository due to GitHub's file size limitations.

### Complaint Dataset

* **NYC 311 Service Requests Dataset**

  * https://www.kaggle.com/datasets/new-york-city/ny-311-service-requests/data

### Image Dataset

* **Garbage, Pothole and Normal Image Dataset**

  * https://data.mendeley.com/datasets/zndzygc3p3

The trained Machine Learning models are already included in the **models/** folder.

---

## 👩‍💻 Developer

**Uddanti Bhavana**

B.Tech – Computer Science and Engineering

R.V.R. & J.C. College of Engineering

---

## 🙏 Acknowledgements

- AICTE
- Edunet Foundation
- IBM SkillsBuild
- Streamlit
- TensorFlow
- Scikit-learn
- Python Software Foundation

---

## ⭐ If you found this project useful, consider giving it a Star on GitHub.