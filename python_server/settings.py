import os
from dotenv import load_dotenv
# Make sure to have API Key's, etc. saved to your local environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
SERVICE_URL = os.getenv("SERVICE_URL")