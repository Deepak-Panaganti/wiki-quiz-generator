# backend/init_db.py
from database import engine
from models import Base

def init():
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized (tables created)")

if __name__ == "__main__":
    init()
