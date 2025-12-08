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
git clone https://github.com/YOUR_USERNAME/Capstone_Project.git  
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

## Contact
**Derrick K. Gibbs-McGlaston**  
Email: derrickkgibbs@gmail.com  
GitHub: https://github.com/dgibbs20
