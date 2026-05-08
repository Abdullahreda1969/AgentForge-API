
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
APP_NAME = "My Application"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
