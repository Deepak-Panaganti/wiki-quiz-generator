# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse
# from scraper import scrape_wikipedia
# from llm import generate_quiz

# app = FastAPI(title="Wiki Quiz Generator")

# @app.post("/generate-quiz")
# def generate_quiz_api(url: str = Query(...)):
#     try:
#         content = scrape_wikipedia(url)
#         result = generate_quiz(content)
#         return JSONResponse(content=result)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse
# from scraper import scrape_wikipedia
# from llm import generate_quiz

# app = FastAPI(title="Wiki Quiz Generator")

# @app.post("/generate-quiz")
# def generate_quiz_api(url: str = Query(...)):
#     try:
#         content = scrape_wikipedia(url)
#         result = generate_quiz(content)
#         return JSONResponse(content=result)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # backend/main.py

# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse
# from scraper import scrape_wikipedia
# from llm import generate_quiz

# app = FastAPI(title="Wiki Quiz Generator")

# @app.post("/generate-quiz")
# def generate_quiz_api(
#     url: str = Query(...),
#     num_questions: int = Query(5, ge=1, le=10),
#     difficulty: str = Query(None, regex="^(easy|medium|hard)$")
# ):
#     try:
#         content = scrape_wikipedia(url)
#         result = generate_quiz(content)

#         # Filter by difficulty
#         if difficulty:
#             result["quiz"] = [
#                 q for q in result["quiz"]
#                 if q["difficulty"] == difficulty
#             ]

#         # Limit number of questions
#         result["quiz"] = result["quiz"][:num_questions]

#         return JSONResponse(content=result)

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))



# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse
# from scraper import scrape_wikipedia
# from llm import generate_quiz

# app = FastAPI(title="Wiki Quiz Generator")

# @app.post("/generate-quiz")
# def generate_quiz_api(
#     url: str = Query(...),
#     num_questions: int = Query(5, ge=1, le=10),
#     difficulty: str | None = Query(None, pattern="^(easy|medium|hard)$")

# ):
#     try:
#         content = scrape_wikipedia(url)
#         result = generate_quiz(content)

#         quiz = result.get("quiz", [])

#         # ✅ FILTER difficulty (backend control)
#         if difficulty:
#             quiz = [q for q in quiz if q["difficulty"] == difficulty]

#         # ✅ LIMIT count
#         quiz = quiz[:num_questions]

#         # ✅ PROFESSIONAL fallback
#         if len(quiz) < num_questions:
#             result["note"] = (
#                 f"Only {len(quiz)} questions available for difficulty='{difficulty}'."
#             )

#         result["quiz"] = quiz
#         return JSONResponse(content=result)

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))




# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse


# from scraper import scrape_wikipedia
# from llm import generate_quiz

# app = FastAPI(title="Wiki Quiz Generator")

# @app.post("/generate-quiz")
# def generate_quiz_api(
#     url: str = Query(..., description="Wikipedia article URL"),
#     num_questions: int = Query(5, ge=1, le=10, description="Number of quiz questions"),
#     difficulty: str | None = Query(
#         None,
#         pattern="^(easy|medium|hard)$",
#         description="Difficulty level"
#     )
# ):
#     try:
#         # 1️⃣ Scrape Wikipedia content
#         content = scrape_wikipedia(url)

#         # 2️⃣ Generate quiz using LLM
#         result = generate_quiz(content)

#         # 3️⃣ Get quiz list safely
#         quiz = result.get("quiz", [])

#         # 4️⃣ Filter by difficulty (backend-controlled)
#         if difficulty:
#             quiz = [q for q in quiz if q.get("difficulty") == difficulty]
#         # 5️⃣ Limit number of questions
#         quiz = quiz[:num_questions]

#         # 6️⃣ Professional fallback message
#         if len(quiz) < num_questions:
#             result["note"] = (
#                 f"Only {len(quiz)} questions available for difficulty='{difficulty}'."
#             )

#         # 7️⃣ Return final response
#         result["quiz"] = quiz
#         return JSONResponse(content=result)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))




# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# from scraper import scrape_wikipedia
# from llm import generate_quiz

# from database import SessionLocal
# from models import QuizHistory

# app = FastAPI(title="Wiki Quiz Generator")

# # Allow local frontend to call API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000", "*"],  # use "*" for dev only
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.post("/generate-quiz")
# def generate_quiz_api(
#     url: str = Query(..., description="Wikipedia article URL"),
#     num_questions: int = Query(5, ge=1, le=10, description="Number of quiz questions"),
#     difficulty: str | None = Query(None, pattern="^(easy|medium|hard)$", description="Difficulty")
# ):
#     try:
#         content = scrape_wikipedia(url)
#         result = generate_quiz(content)

#         if not isinstance(result, dict):
#             raise ValueError("Invalid JSON returned from LLM")

#         quiz = result.get("quiz", [])
#         related_topics = result.get("related_topics", [])

#         # backend filtering (optional)
#         if difficulty:
#             quiz = [q for q in quiz if q.get("difficulty") == difficulty]

#         quiz = quiz[:num_questions]

#         # Save to DB
#         db = SessionLocal()
#         record = QuizHistory(
#             url=url,
#             quiz=quiz,
#             related_topics=related_topics or []
#         )
#         db.add(record)
#         db.commit()
#         db.refresh(record)  # populate id
#         db.close()

#         return JSONResponse({
#             "id": record.id,
#             "quiz": quiz,
#             "related_topics": related_topics
#         })

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @app.get("/history")
# def get_history():
#     db = SessionLocal()
#     records = db.query(QuizHistory).order_by(QuizHistory.id.desc()).all()
#     db.close()
#     return [{"id": r.id, "url": r.url} for r in records]


# @app.get("/history/{quiz_id}")
# def get_history_detail(quiz_id: int):
#     db = SessionLocal()
#     record = db.query(QuizHistory).filter(QuizHistory.id == quiz_id).first()
#     db.close()
#     if not record:
#         raise HTTPException(status_code=404, detail="Quiz not found")
#     return {
#         "id": record.id,
#         "url": record.url,
#         "quiz": record.quiz,
#         "related_topics": record.related_topics
#     }

# backend/main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from scraper import scrape_wikipedia
from llm import generate_quiz
from database import SessionLocal
from models import QuizHistory

app = FastAPI(title="Wiki Quiz Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-quiz")
def generate_quiz_api(
    url: str = Query(...),
    num_questions: int = Query(5, ge=1, le=10),
    difficulty: str | None = Query(None, pattern="^(easy|medium|hard)$")
):
    try:
        scraped = scrape_wikipedia(url)

        result = generate_quiz(scraped["content"])

        quiz = result.get("quiz", [])
        related_topics = result.get("related_topics", [])

        if difficulty:
            quiz = [q for q in quiz if q.get("difficulty") == difficulty]

        quiz = quiz[:num_questions]

        db = SessionLocal()
        record = QuizHistory(
            url=url,
            title=scraped.get("title"),
            summary=scraped.get("summary"),
            sections=scraped.get("sections"),
            quiz=quiz,
            related_topics=related_topics
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        db.close()

        return JSONResponse({
            "id": record.id,
            "url": url,
            "title": record.title,
            "summary": record.summary,
            "quiz": quiz,
            "related_topics": related_topics
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/history")
def get_history():
    db = SessionLocal()
    rows = db.query(QuizHistory).order_by(QuizHistory.id.desc()).all()
    db.close()
    return [{"id": r.id, "url": r.url, "title": r.title} for r in rows]


@app.get("/history/{quiz_id}")
def get_history_detail(quiz_id: int):
    db = SessionLocal()
    r = db.query(QuizHistory).filter(QuizHistory.id == quiz_id).first()
    db.close()

    if not r:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {
        "id": r.id,
        "url": r.url,
        "title": r.title,
        "summary": r.summary,
        "sections": r.sections,
        "quiz": r.quiz,
        "related_topics": r.related_topics
    }
