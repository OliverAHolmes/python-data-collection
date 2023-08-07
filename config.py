import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    if ENV == "testing":
        db_path = "test.db"
    else:
        db_path = "database.db"

settings = Settings()
