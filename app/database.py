import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    load_dotenv()
    print(f"DATABASE_URL={os.environ.get('DATABASE_URL')}\n")
except Exception:
    pass

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)