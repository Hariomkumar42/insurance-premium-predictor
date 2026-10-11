# 🏥 Insurance Premium Predictor

**A Machine Learning Web Application using Python, FastAPI and Streamlit**

## 📌 Overview

Insurance Premium Predictor is a machine learning project that uses user-provided information to predict an insurance premium category. It demonstrates how a trained machine learning model can be integrated into a web application through a REST API and an interactive frontend.

## ✨ Features

- Interactive Streamlit user interface
- FastAPI backend for prediction requests
- Machine learning inference using a saved model
- Input processing, including BMI and derived features
- REST API documentation through Swagger UI
- Modular frontend and backend architecture

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- FastAPI
- Streamlit
- Pydantic
- Uvicorn
- Git and GitHub

## 🏗️ Architecture

```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI REST API
  ↓
Input Processing
  ↓
Trained ML Model
  ↓
Predicted Category
  ↓
Result Display
```

## 📂 Project Structure

```text
insurance-premium-predictor/
├── app.py
├── streamlit_app.py
├── model.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Hariomkumar42/insurance-premium-predictor.git
cd insurance-premium-predictor
```

### 2. Create and activate a virtual environment

```bash
python -m venv myenv
```

Windows PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The saved model was trained using scikit-learn 1.6.1. Use a compatible version when loading the model.

### 4. Run the FastAPI backend

```bash
uvicorn app:app --reload
```

API URL: http://127.0.0.1:8000

Interactive API documentation: http://127.0.0.1:8000/docs

### 5. Run the Streamlit frontend

Open a second terminal and run:

```bash
streamlit run streamlit_app.py
```

Keep the FastAPI backend running while using the frontend.

## 🔌 API Endpoint

**POST `/predict`**

Accepts user information as JSON and returns the predicted category from the trained model.

Use the interactive Swagger documentation at `/docs` to inspect the exact input fields and test the endpoint.

## 🧠 Machine Learning Workflow

1. Collect user input.
2. Validate and process input features.
3. Calculate derived features required by the model.
4. Prepare a Pandas DataFrame.
5. Generate a prediction using the saved model.
6. Return the result through FastAPI.
7. Display the result in Streamlit.

## 🔮 Future Improvements

- Deploy the application online.
- Add automated tests and stronger error handling.
- Evaluate and document model performance using appropriate metrics.
- Add application screenshots and a live demo.
- Improve model versioning and reproducibility.

## 👨‍💻 Author

**Hariom Kumar**

MCA Student | Aspiring Data Scientist and AI Engineer


GitHub: [Hariomkumar42](https://github.com/Hariomkumar42)

## 📸 Project Screenshots

### Streamlit Frontend
Screenshot 2026-10-12 021110.png

### Prediction Result
Screenshot 2026-10-12 021156.png,Screenshot 2026-10-12 021210.png


## ⚠️ Disclaimer

This project is for educational and demonstration purposes only. Predictions are model estimates and should not be treated as official insurance quotes or financial advice.
