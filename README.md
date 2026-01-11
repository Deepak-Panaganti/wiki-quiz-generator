# **Wiki Quiz Generator (Wikipedia → AI Quiz)**  
### _LLM-Based Quiz Generation Assignment_  
**Author:** Deepak Panaganti  

---

<br>

## 🚀 **Tech Stack**
- **Frontend:** HTML, CSS, Vanilla JavaScript  
- **Backend:** Python (FastAPI)  
- **Database:** PostgreSQL (SQLite for local testing)  
- **LLM:** Google Gemini (via LangChain)  
- **Web Scraping:** BeautifulSoup  

---

<br>

## 📌 **Project Overview**
A full-stack **AI-powered Wiki Quiz Generator** that transforms Wikipedia articles into structured quizzes using a Large Language Model.

Users can:

- Provide a Wikipedia article URL  
- Automatically generate quizzes using AI  
- View multiple-choice questions  
- See difficulty levels and explanations  
- Store and revisit past quizzes  

This project demonstrates **real-world LLM integration**, backend-driven UI, and database persistence.

---

<br>

# ✅ **1. Frontend (HTML + CSS + JavaScript)**

## ✔ **Included Screens**
- Quiz Generation Page (Tab 1)  
- Quiz Result Cards  
- History Page (Tab 2)  
- Quiz Details Modal  

<br>

## ⭐ **Frontend Features**
- Clean and minimal UI  
- Two-tab layout (Generate Quiz / History)  
- Card-based quiz display  
- Difficulty badges (easy / medium / hard)  
- “Show Answer & Explanation” toggle  
- Modal popup for viewing quiz history  
- Fully backend-driven (no frontend framework dependency)  

---

<br>

# ✅ **2. Backend (FastAPI)**

## ⭐ **Backend Features**
- RESTful API built using FastAPI  
- Wikipedia content scraping with BeautifulSoup  
- AI-powered quiz generation via LangChain + Google Gemini  
- Structured JSON API responses  
- Quiz persistence in PostgreSQL database  
- Quiz history retrieval with detailed view  
- Robust error handling for:  
  - Invalid Wikipedia URLs  
  - Empty or malformed LLM responses  
  - API quota and rate-limit issues  

---

<br>

# 📘 **API Endpoints**

## 🧠 Generate Quiz  
| Method | Endpoint | Description |
|------|---------|-------------|
| **POST** | `/generate-quiz` | Generate quiz from Wikipedia URL |

### Query Parameters
- `url` → Wikipedia article URL  
- `num_questions` → Number of questions (1–10)  
- `difficulty` → easy / medium / hard (optional)  

<br>

## 📜 Quiz History  
| Method | Endpoint | Description |
|------|---------|-------------|
| **GET** | `/history` | Fetch all past quizzes |
| **GET** | `/history/{quiz_id}` | Fetch quiz details |

---

<br>

# ✅ **3. Database (PostgreSQL / SQLite)**

## **ENTITY–RELATIONSHIP DIAGRAM (ERD)**
┌─────────────────────┐
│ quizzes             │
├─────────────────────┤
│ id (PK)             │
│ url                 │
│ title               │
│ summary             │
│ quiz (JSON)         │
│ related_topics(JSON)│
└─────────────────────┘
---

| quizzes |
|------|---------|-------------|
| ** id (PK)** |
| **GET** | `/history/{quiz_id}` | Fetch quiz details |

---

<br>

Each quiz record stores:
- Source Wikipedia URL  
- Generated quiz questions  
- Difficulty levels & explanations  
- AI-suggested related topics  

---

<br>

## ✔ **Sample Data Included**
- Wikipedia URLs tested:
  - Alan Turing  
  - Artificial Intelligence  
- Corresponding generated quiz JSON outputs  

---

<br>

# ✅ **4. Documentation (As Required)**

## 🚀 **Setup Guide**

## 🔧 Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Initialize Database
```
python init_db.py
```

## Start Backend Server
```
uvicorn main:app --reload
```

## Backend runs at:
👉 http://127.0.0.1:8000

<br>

## 🧩 Environment Variables

-Create a .env file inside backend/ (NOT pushed to GitHub):
```
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/wikiquiz
```
<br>

## 💻 Frontend Setup

```
cd frontend
```
-Open index.html directly
-OR use Live Server in VS Code
-Frontend runs at:
👉 http://127.0.0.1:5500

<br>

## 🌟 Feature Summary

# **📘 Wikipedia-based quiz generation:**
- 🤖 AI-powered question creation using Gemini
- 🧠 Difficulty-based filtering
- 💾 Persistent quiz history
- 📊 Structured JSON API responses
- 🧾 Modal-based quiz review
- 🧼 Clean and minimal UI

<br>

## 🏁 Conclusion

# **This Wiki Quiz Generator demonstrates:**
- End-to-end AI integration using LangChain
- Clean Wikipedia scraping and data extraction
- Backend-driven frontend architecture
- Database-backed quiz history
- Practical real-world use of Large Language Models
-Strong API design with proper error handling

<br>

🙏 Thank You

Wiki Quiz Generator

Developed by Deepak Panaganti ✅

