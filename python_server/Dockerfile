# Python
FROM python:3
COPY ./ /smart_meetings/python_server
WORKDIR /smart_meetings/python_server
RUN pip install -r requirements.txt
RUN python3 main.py