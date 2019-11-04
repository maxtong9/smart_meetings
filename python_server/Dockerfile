# Python
FROM python:3

# Set environment variables
# Values will be passed on from command line
# USE .env FILE INSTEAD
# ARG WATSON_API_KEY
# ARG SERVICE_URL
# ENV WATSON_API_KEY=$WATSON_API_KEY
# ENV SERVICE_URL=$SERVICE_URL

WORKDIR /smart_meetings/python_server/

# Copy and install requirements.txt and nltk
COPY requirements.txt install_nltk.py ./
RUN pip install -r requirements.txt \
 && python install_nltk.py

# Copy the rest of the files
COPY . .

# Run the script
RUN python main.py
