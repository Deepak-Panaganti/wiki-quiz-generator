# from pydantic import BaseModel
# from typing import List, Dict, Any

# class QuizResponse(BaseModel):
#     id: int
#     url: str
#     title: str
#     summary: str
#     sections: List[str]
#     quiz: List[Dict[str, Any]]
#     related_topics: List[str]


# backend/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Question(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizResponse(BaseModel):
    id: Optional[int]
    url: str
    title: Optional[str]
    summary: Optional[str]
    sections: Optional[List[str]]
    quiz: List[Dict[str, Any]]
    related_topics: List[str]
