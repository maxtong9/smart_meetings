# Python
FROM python:3
COPY /python_server /smart_meetings/python_server
WORKDIR /smart_meetings/python_server
RUN pip install -r requirements.txt
ENV API_KEY 8W_8axK4MIt2HRV4iAFNUe8q2uOV_GpOg5lHAXWu51Tw
ENV SERVICE_URL https://stream.watsonplatform.net/speech-to-text/api
RUN python3 main.py

# Ruby on Rails
# FROM ruby:2.6.5
# COPY /rails_hw /ruby_on_rails_app
# WORKDIR /ruby_on_rails_app