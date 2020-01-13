import os
from dotenv import load_dotenv
# Make sure to have API Key's, etc. saved to your local environment variables
load_dotenv()
WATSON_API_KEY = os.getenv("WATSON_API_KEY")
SERVICE_URL = os.getenv("SERVICE_URL")
# print("WATSON_API_KEY: "+ WATSON_API_KEY)
# print("SERVICE_URL: " + SERVICE_URL)
