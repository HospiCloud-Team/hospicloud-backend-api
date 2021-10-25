from common.models import SessionLocal, create_tables

def get_db():
    create_tables()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()