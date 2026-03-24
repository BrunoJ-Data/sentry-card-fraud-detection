# 🛡️ Sentry – Fraud card Detection Engine


This project was developed during my intensive Data Analysis program.  
It simulates a **real-time card banking fraud detection system** combining **Machine Learning** and **rule-based detection**.

I wanted a user friendly interface, focusing on most important.
 The system compares incoming transactions against a "Customer Profile" ( average spending, usual distance from home) which is stored in internal database.



The objective is to detect suspicious credit card transactions by analyzing customer behavior and transaction anomalies.
https://sentry-fraud-detector.streamlit.app
---

# 🎯 Project Overview

The system analyzes **credit card transactions** and evaluates the probability of fraud using:

- A **Machine Learning model**
- **Business rules** commonly used in fraud detection systems

The project is based on a **Kaggle dataset containing ~1 million transactions**.

---

# 📊 Dataset & Feature Engineering

Data was cleaned and processed using **Pandas**.

Key features used in the model include:

- Transaction **amount**
- **Hour of the day**
- **Day of the week**

Additional behavioral features were engineered:

- **Average distance from customer's usual location**
- **Spending deviation ratio** compared to the customer's historical average
- Detection of **unusual merchant categories**

These features help simulate a **behavioral fraud detection approach**.

---

# 🤖 Machine Learning Model

The system uses:

- **XGBoost classifier**
- Built with **Scikit-Learn pipeline**

The model outputs a **fraud probability score**, which is then combined with rule-based alerts.

---

# 🟢 Fraud Detection Logic

The system flags suspicious transactions based on:

- Amount **> 3x the customer's average spending**
- **Unusual geographic distance**
- Merchant categories never used before**

This creates a **hybrid detection engine** combining ML predictions and business rules.

---

# 🖥️ Interactive Dashboard

A **Streamlit dashboard** allows users to:

- Simulate transactions
- View fraud probability scores
- Trigger rule-based alerts

Live Demo:

https://sentry-fraud-detector.streamlit.app

---

# 🛠️ Tech Stack

**Language**

- Python 3

**Libraries**

- Pandas
- Scikit-Learn
- XGBoost
- Joblib

**Tools**

- VS Code
- Google Colab
- Streamlit

---

# 🔮 Future Improvements

Next development steps:

- Add a **batch processing system** for large-scale transaction analysis


---

# 📌 Project Goal

This project aims to demonstrate how **machine learning and rule-based systems can be combined to detect financial fraud**
by using a user-friendly interface.
