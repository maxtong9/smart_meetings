# Python
FROM python:3
COPY /speech_to_text /speech_to_text
WORKDIR /speech_to_text
RUN pip install -r requirements.txt
ENV API_KEY 8W_8axK4MIt2HRV4iAFNUe8q2uOV_GpOg5lHAXWu51Tw
ENV SERVICE_URL https://stream.watsonplatform.net/speech-to-text/api
CMD [ "python3", "main.py" ]
COPY requirements.txt /speech_to_text/requirements.txt

# Ruby on Rails