from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import getenv

load_dotenv()

engine = create_engine(f"postgresql://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}/{getenv("DB_NAME")}",
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)