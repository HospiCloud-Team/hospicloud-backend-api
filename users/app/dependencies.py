from common.models import SessionLocal, Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()