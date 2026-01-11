# from sqlalchemy import Column, Integer, String, JSON
# from database import Base

# class Quiz(Base):
#     __tablename__ = "quizzes"

#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String, nullable=False)
#     title = Column(String, nullable=False)
#     summary = Column(String)
#     sections = Column(JSON)
#     quiz = Column(JSON)
#     related_topics = Column(JSON)


# from sqlalchemy import Column, Integer, String, JSON
# from database import Base

# class QuizHistory(Base):
#     __tablename__ = "quiz_history"

#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String, nullable=False)
#     quiz = Column(JSON, nullable=False)
#     related_topics = Column(JSON, nullable=False)






# backend/models.py
from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from database import Base

class QuizHistory(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)

    # MUST be nullable
    title = Column(String, nullable=True)
    summary = Column(String, nullable=True)

    sections = Column(JSON, nullable=True)
    quiz = Column(JSON, nullable=True)
    related_topics = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
