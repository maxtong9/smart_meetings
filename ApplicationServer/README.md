# Rails Local Environment MacOS Setup

## Install Homebrew

First, Install Homebrew. Homebrew allows installation and compilation of software packages easily from source.  
`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"` 

## Install rbenv

To do this, run the following commands in your Terminal:  
`brew install rbenv ruby-build`  
`echo 'if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi' >> ~/.bash_profile
source ~/.bash_profile 
`

## Install Ruby

`rbenv install 2.6.5`  
`rbenv global 2.6.5`  

Check version:  
`ruby -v`

## Install Rails version 6.0.0

`gem install rails -v 6.0.0`  
`rbenv rehash`  

Check version:  
`rails -v`

## Install Nodejs version 13.0.0

`brew install node`  

Check node version and npm version:  
`node -v`  
`npm -v`

## Install Gems in Gemfile

`bundle install`

## Install node_modules folder

`npm install`

## Install yarn

`brew install yarn`

## Update Yarn packages

`yarn install --check-files`

## Run application

Run in Rails application directory:  
`rails s`

Then locate to http://localhost:3000/.

# Rails Local Environment End-to-End Testing

## Install PostgreSQL locally (for MacOS)

This is a full PostgreSQL installation packaged as a Mac application.  
https://postgresapp.com/  
Follow the instructions through the link.

## Starting PostgreSQL server

Open the Postgres.app application installed in the previous step.  
Server should automatically initialize.

## Create PostgreSQL role

This will create a new PostgreSQL role.  
`sudo -u postgres createuser -s applicationserver`

## Install Gems in Gemfile

`bundle install`

## Install node_modules folder

`npm install`

## Update Yarn packages

`yarn install --check-files`

## Create and Migrate database

```
rails db:setup
rails db:migrate
```

## Create test.json file to upload while creating user (can just be anywhere) with:

This step is only relevant up until our text analysis functions are working.

`{"id":1,"name":"File Name","transcription":"hahaha","questions": ["how", "when"],"summary":"heywassupyo", "action_items": ["do", "this"]}`

## Testing

run `rails s`

Make sure the socket is running (Refer to the python_server documentation)

Then locate to http://localhost:3000/users/new.

Add a new user and upload test.json to it.

Click Back, then click Show on the user you just created and witness the marvel.
