# Text and Audio Processor (python3)

* This directory has two Parts: The Text Processor, and the Audio Processor


### Setup

* Python Version: 3
* Install Dependencies via pip3 with `pip3 install -r requirements.txt`
* Download all nltk libs (until we single out which ones we use) with:
* In a python3 Shell, run the following 2 commands: 
```
import nltk
nltk.download('all')
```

### References

#### Text Processor

* [nltk](https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk)
* [Python Sockets](https://realpython.com/python-sockets/)
* [Summarizing Text](https://stackabuse.com/text-summarization-with-nltk-in-python/)

#### Audio Processor

* [Speech Recognition](https://cloud.ibm.com/docs/services/speech-to-text?topic=speech-to-text-http#HTTP-basic)

## Docker

### Environment variables

Environment variables are located in the .env file. They are automatically loaded by Docker, so it is not necessary to set the environment variables on the host machine.

The .env file is in the .gitignore. If you wish to commit it to GitHub, create a local branch and commit to there without pushing.

### Build image

`docker image build -t christinatao31/smart_meetings:python_server_v1 .`

### Run container

`docker container run --env-file .env --name ps christinatao31/smart_meetings:python_server_v1`

#### Run container in interactive mode

To start the container's bash shell:

`docker container run -it --name ps christinatao31/smart_meetings:python_server_v1 bash`
