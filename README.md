# smart_meetings
CS Capstone Project. Make Meetings Smarter! With Smart Meetings...

# Local Installation & Setup Instructions:
- Please clone or zip/unzip the repo to your desired workspace.

# End-to-End Testing

## Install PostgreSQL locally (for MacOS)

This is a full PostgreSQL installation packaged as a Mac application.  
https://postgresapp.com/  
Follow the instructions through the link

## Starting PostgreSQL server

Open the Postgres.app application installed in the previous step.  
Server should automatically initialize.

## Update PostgreSQL role

Change database role to your operating system user:  
Open `ApplicationServer/config/database.yml`.  
On line 32, change the username to your operating system username.

## Install Gems in Gemfile

`bundle install`

## Install node_modules folder

`npm install`

## Update Yarn packages

`yarn install --check-files`

## Setup and Migrate database

Go into the Rails application directory.  
```
rake db:setup
rake db:migrate
```

## Install awscli for Python aws credentials

`pip3 install awscli`

then set credentials using:  
`aws configure`

Then enter the Id and Secret Key shared in the group chat.  
region: us-west-1

## Rails credentials

Put shared master.key file (messenger) into  
`smart_meetings/ApplicationServer/config`

## Create test.json file to upload while creating user (can just be anywhere) with:

This step is only relevant up until our text analysis functions are working.

`{"id":1,"name":"File Name","transcription":"hahaha","questions": ["how", "when"],"summary":"heywassupyo", "action_items": ["do", "this"]}`

## Start Python Socket

In a different terminal, go into the `python_server` directory and run:  
`pip3 install -r requirements.txt`  
`python3 socket_listener.py`

## Testing

run `rails s`

Then locate to http://localhost:3000/meetings/new.

Add a new meeting and upload test.json to it.

Click Back, then click Show on the meeting you just created and witness the marvel.

# How to run Docker

## Docker compose

<!-- `docker-compose run app yarn` -->

Comment/uncomment the marked lines in ApplicationServer/config/database.yml, python_server/main.py, ApplicationServer/app/controllers/users_controller.rb

`docker-compose build`

`docker-compose run app rake db:setup`

`docker-compose run app rake db:migrate`

`docker-compose up`

To bring everything down and remove containers completely:

`docker-compose down`

## Install Docker Desktop

<https://hub.docker.com/?overlay=onboarding>

## Tutorials used

<https://docs.docker.com/get-started/>
<https://docker-curriculum.com/>
<https://blog.codeship.com/running-rails-development-environment-docker/>
