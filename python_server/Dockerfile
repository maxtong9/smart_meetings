# Python
FROM python:3
COPY ./ /smart_meetings/python_server
WORKDIR /smart_meetings/python_server
RUN pip install -r requirements.txt
ENV API_KEY 8W_8axK4MIt2HRV4iAFNUe8q2uOV_GpOg5lHAXWu51Tw
ENV SERVICE_URL https://stream.watsonplatform.net/speech-to-text/api
RUN python3 main.py