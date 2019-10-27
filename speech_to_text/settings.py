import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
SERVICE_URL = os.getenv("SERVICE_URL")