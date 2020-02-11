# Python
FROM python:3

# Set environment variables
# Values will be passed on from command line
# USE .env FILE INSTEAD
# ARG WATSON_API_KEY
# ARG SERVICE_URL
# ARG AWS_ACCESS_KEY_ID
# ARG AWS_SECRET_ACCESS_KEY
# ARG AWS_DEFAULT_REGION
# ENV WATSON_API_KEY=$WATSON_API_KEY
# ENV SERVICE_URL=$SERVICE_URL
# ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
# ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
# ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

WORKDIR /smart_meetings/python_server/

# Copy and install requirements.txt and nltk
COPY requirements.txt nltk_downloader_script.py ./
RUN pip install -r requirements.txt \
 && python nltk_downloader_script.py

# Install and configure aws cli
# RUN pip install awscli
# RUN aws configure

# Copy the rest of the files
COPY . .

# Run the script
CMD python main.py
