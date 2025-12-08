<img width="1536" height="1024" alt="1" src="https://github.com/user-attachments/assets/6a0c6118-ab86-4b45-a39d-2c4c5a6d7991" />

## Tech Stack

| Area          | Technologies Used |
|---------------|-------------------|
| Language      | Python 3.10 |
| Backend API   | FastAPI |
| Machine Learning | Scikit-Learn (TF-IDF + LinearSVC) |
| Frontend      | HTML, CSS, JavaScript |
| Database      | SQLite |
| Tools         | Uvicorn, Pandas, Joblib |
| Version Control | Git & GitHub |


![GitHub last commit](https://img.shields.io/github/last-commit/dgibbs20/Capstone_Project)
![GitHub repo size](https://img.shields.io/github/repo-size/dgibbs20/Capstone_Project)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)


# Smart Budgeting Agent — Capstone Project (ITAI-2277)
**Author:** Derrick K. Gibbs-McGlaston  
**Instructor:** Sitaram Ayyagari  
**Course:** Artificial Intelligence Programming — Capstone  
**Semester:** Fall 2025  


## Project Overview
The Smart Budgeting Agent is a full-stack AI application that automatically categorizes financial transactions using a machine learning model trained on real-world spending patterns. This project demonstrates mastery of:
- Machine learning model development  
- Data preprocessing and feature engineering  
- API design with FastAPI  
- Frontend integration with JavaScript  
- Database persistence using SQLite  
- Full-stack AI system architecture and deployment structure  
This repository includes the complete, installable project ready for evaluation and demonstration.

## Repository Structure
Capstone_Project/  
│  
├── backend/                 # FastAPI backend + ML model logic  
│   ├── app.py               # API routes (predict, transactions)  
│   ├── db.py                # SQLite database handling  
│   ├── schema.sql           # Database schema  
│   ├── train_pipeline.py    # ML training script  
│   ├── model_pipeline.pkl   # Final trained ML model  
│   ├── decision_tree_expenses.pkl  
│   ├── expenses_preprocessed.csv  
│   ├── metrics/  
│   └── app.db  
│  
├── frontend/  
│   ├── index.html  
│   ├── app.js  
│   └── styles.css  
│  
├── tests/  
├── requirements.txt  
└── README.md  

## Installation & Setup Instructions
### 1. Clone the Repository
git clone https://github.com/dgibbs20/Capstone_Project.git  
cd Capstone_Project  

### 2. Create & Activate Virtual Environment
python3 -m venv .venv  
source .venv/bin/activate  

### 3. Install Dependencies
pip install -r requirements.txt  
## Running the Application

### Step 1: Initialize the Database
cd backend  
python db.py  

### Step 2: Launch Backend API
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000  

### Step 3: Open the Frontend
Open:  
frontend/index.html  
This loads the UI, allowing:
- Transaction entry  
- Automatic category prediction  
- Saving to database  
- End-to-end system interaction  

## Machine Learning Model
Model: Support Vector Classifier (Linear SVC)  
Pipeline: TF-IDF Vectorizer → Linear SVC  
Performance: ~90% accuracy  
Metrics are stored in:  
/backend/metrics/  

## Capstone Requirements Covered
- Full-stack AI system  
- Machine learning model + pipeline  
- Frontend UI  
- FastAPI backend  
- SQLite database  
- Documentation  
- GitHub repo with full installation instructions  
- Ready for instructor testing  


## Demo & Screenshots

Below are screenshots demonstrating the Smart Budgeting Agent in action.

### Application Homepage
<img width="1496" height="967" alt="Screenshot 2025-12-03 at 1 38 52 PM" src="https://github.com/user-attachments/assets/1d645046-e5c4-42c5-add6-ba8f41257c96" />

### Transaction Prediction Example
<img width="1496" height="967" alt="Screenshot 2025-12-03 at 1 44 06 PM" src="https://github.com/user-attachments/assets/8672785f-7231-44bb-a4e8-7bc9cc4e823f" />


These images show:
- The working frontend UI
- The prediction interface
- End-to-end system operation

  
## Contact
Derrick K. Gibbs-McGlaston  
Email: derrickkgibbs@gmail.com  
GitHub: https://github.com/dgibbs20  
