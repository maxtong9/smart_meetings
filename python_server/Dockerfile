# Python
FROM python:3

# Set environment variables
# Values will be passed on from command line
ARG WATSON_API_KEY
ARG SERVICE_URL
ENV WATSON_API_KEY=$WATSON_API_KEY
ENV SERVICE_URL=$SERVICE_URL

# Copy files
WORKDIR /smart_meetings/python_server/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Run the script
RUN python3 main.py
