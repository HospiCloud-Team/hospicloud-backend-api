import os
from sqlalchemy import create_engine


def start_engine():
    db_host = os.getenv("DB_HOST", "postgres-db:5432")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_name = os.getenv("DB_NAME", "postgres")

    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")
    return engine
