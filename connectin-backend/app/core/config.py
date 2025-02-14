import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings(BaseSettings):
    # ... существующие поля
    DATABASE_URL: str
    SECRET_KEY: str
    
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_REDIRECT_URI: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    
    # AWS_ACCESS_KEY_ID = str
    # AWS_SECRET_ACCESS_KEY = str
    # AWS_BUCKET_NAME = str
    # AWS_REGION = str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global instance of settings
settings = Settings()
