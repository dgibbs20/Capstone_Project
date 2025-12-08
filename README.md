Smart Budgeting Agent — User Guide (Phase 05)
Student: Derrick K. Gibbs-McGlaston
Course: 6261-ITAI-2277 — Artificial Intel Resource

⸻

1. Overview

The Smart Budgeting Agent is a simple web-based tool that helps a user track spending and automatically assign categories to each transaction. The system has three main parts:
	•	A FastAPI backend that loads a trained machine learning model, predicts categories, and stores transactions in a SQLite database.
	•	A web frontend (HTML/CSS/JavaScript) where the user can enter new transactions and see recent activity.
	•	A SQLite database that keeps a history of all transactions and their predicted categories.

This guide explains how to install, run, and use the prototype.

⸻

2. Installation

Prerequisites
	•	Python 3.10+ installed on your machine
	•	pip available
	•	The project folder: smart_budgeting_mvp/

Steps
	1.	Open a terminal and navigate to the project root:
		cd /path/to/smart_budgeting_mvp

	2.	Create and activate a virtual environment:
		python3 -m venv .venv
		source .venv/bin/activate

	3.	Install dependencies:
		pip install -r requirements.txt

	

3. Running the Backend API
	1.	In the same terminal, move into the backend folder:
		cd backend

	2.	Initialize the SQLite database:
		python db.py

	This creates app.db with the required transactions table.

	3.	Start the FastAPI server:
		python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

	4.	Once the server is running, you can open the automatic API documentation in a browser:
		http://127.0.0.1:8000/docs￼

	There you can see the available endpoints and try them directly.

4. Running the Frontend (Web UI)
	1.	Open a new terminal window or tab.

	2.	From the project root, run a simple static file server:
		cd /path/to/smart_budgeting_mvp
		python -m http.server 5173

		3.	In your browser, open:
	•	http://127.0.0.1:5173/frontend/index.html￼

You should see the Smart Budgeting Agent interface: a form at the top and a Recent Transactions table below.

⸻

5. Using the Application

Add a new transaction
	1.	In the “Add Transaction” form, fill in:
	•	Description (e.g., “Grande Latte”)
	•	Merchant (e.g., “Starbucks”)
	•	Amount ($) (e.g., 6.25)
	•	Payment Method (e.g., “Debit Card”)
	2.	Click Predict & Save.
	3.	The backend will:
	•	Build features from the transaction (amount, date, weekend flag, payment method, and text),
	•	Use the ML model to predict the category,
	•	Store the transaction and its predicted category in the SQLite database.
	4.	The UI will display:
	•	A short message: “Predicted: <Category>”
	•	A new row in the Recent Transactions table with:
	•	Date and time
	•	Description
	•	Merchant
	•	Amount
	•	Payment method
	•	Predicted category

Examples
	•	Starbucks coffee purchase → likely Food
	•	Uber ride → likely Transportation

The system also uses a small keyword override layer so well-known vendors (like Starbucks, Uber, or major phone/internet providers) map to appropriate categories even when the base model is uncertain.

⸻

6. Viewing Existing Transactions

The Recent Transactions table at the bottom of the page shows the latest entries pulled from the API.
	•	The frontend calls GET /transactions on the backend.
	•	Transactions are ordered by creation time in descending order (newest first).

If the table appears empty, make sure:
	1.	The backend server is running (no errors in the terminal).
	2.	You have added at least one transaction successfully.

⸻

7. Basic Troubleshooting

Problem: The page loads, but the form does nothing.
Check:
	•	Confirm the backend is running at http://127.0.0.1:8000.
	•	Open http://127.0.0.1:8000/health and look for a JSON response like:
			
			{ "status": "ok", "model_loaded": true }

Problem: I get an error when starting the backend.
Check:
	•	Run pip install -r requirements.txt again to make sure all dependencies are installed.
	•	Ensure decision_tree_expenses.pkl and expenses_preprocessed.csv are in the backend/ folder.

Problem: CORS or network errors in the browser console.
Check:
	•	Make sure you are opening http://127.0.0.1:5173/frontend/index.html, not a file:/// URL.
	•	Always keep the backend running while using the UI.

⸻

8. How the Model Works (High Level)
	•	The model started from the work in earlier phases (Phase 2 and Phase 3).
	•	It uses:
	•	Numeric features like amount, month, day, and is_weekend.
	•	A string feature like payment_method.
	•	Text from description and merchant.
	•	After training, the model file is saved as decision_tree_expenses.pkl and loaded by the FastAPI app at startup.

The current prototype focuses on being simple, explainable, and easy to run on a single machine. It is meant to be a foundation that could eventually grow into a more advanced personal budgeting system.
