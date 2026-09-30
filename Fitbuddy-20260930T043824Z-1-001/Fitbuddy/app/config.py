import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fitbuddy.db"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

WORKOUT_MODEL = os.getenv(
    "WORKOUT_MODEL",
    "gemini-3.6-flash"
)

TIP_MODEL = os.getenv(
    "TIP_MODEL",
    "gemini-3.6-flash"
)

DEMO_MODE = os.getenv(
    "DEMO_MODE",
    "false"
).lower() == "true"