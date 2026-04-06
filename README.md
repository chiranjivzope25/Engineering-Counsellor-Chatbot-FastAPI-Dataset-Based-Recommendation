# 🎓 Engineering Counsellor Chatbot  
### FastAPI + Dataset-Based College Recommendation System

🚀 A smart chatbot that helps students find suitable engineering colleges based on MHT-CET percentile, preferred branch, and location.

---

## 🧠 Overview
This project is designed to simulate a real counselling system used during engineering admissions. It processes user queries in natural language (e.g., "95 percentile CSE Pune") and returns relevant college recommendations using a structured cutoff dataset.

---

## ✨ Key Features
- 🔍 Understands natural user queries  
- 🎯 College recommendation based on percentile, branch & location  
- ⚡ FastAPI backend for fast response  
- 💬 Simple chatbot-style interaction  
- 📊 Dataset-driven decision logic  

---

## 🛠 Tech Stack
- Backend: Python, FastAPI  
- Frontend: Python  
- Data Handling: Pandas  
- Dataset: MHT-CET cutoff-based structured CSV  

---

## 📂 Project Structure
```
counsellor-chatbot/
│── backend/
│   ├── api.py
│   ├── Counseller_chatbot.py
│
│── frontend/
│   ├── Counseller_frontend.py
│
│── dataset/
│   ├── real_cutoff_dataset.csv
│
│── README.md
│── .gitignore
```

---

## ▶️ How to Run Locally

### 1️⃣ Clone Repository
```
git clone https://github.com/chiranjivzope25/Engineering-Counsellor-Chatbot-FastAPI-Dataset-Based-Recommendation.git
cd Engineering-Counsellor-Chatbot-FastAPI-Dataset-Based-Recommendation
```

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 3️⃣ Run Backend
```
uvicorn api:app --reload
```

### 4️⃣ Run Frontend
```
python Counseller_frontend.py
```

---

## 💡 Example Query
```
95 percentile Computer Engineering Pune
```

---

## 📸 Project Preview
(Add your screenshot here)
```
![App Screenshot](screenshot.png)
```

---

## 🚀 Future Improvements
- Integration with real CAP cutoff dataset  
- LLM-based conversational chatbot  
- Advanced filtering (category, rank, fees)  
- Web-based UI deployment  

---

## 🧠 What I Learned
- Building API-based applications using FastAPI  
- Designing dataset-driven recommendation systems  
- Handling user queries and parsing inputs  
- Structuring real-world engineering problems  

---

## 👨‍💻 Author
Chiranjiv Zope  
First Year Engineering Student | AIML Enthusiast  

---

⭐ If you like this project, consider giving it a star!
