# Rails Local Environment MacOS Setup

## Install Homebrew
First, Install Homebrew. Homebrew allows installation and compilation of software packages easily from source.

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

## Install rbenv

To do this, run the following commands in your Terminal:

`brew install rbenv ruby-build`
```
echo 'if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi' >> ~/.bash_profile
source ~/.bash_profile
```

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

Open two terminals in the ApplicationServer directory.

Run:

`rails s`

Then locate to http://localhost:3000/.

On the second window run (Ignore if not making direct changes to application):

`bin/webpack-dev-server`

## Docker

### Two Options

#### Option 1: Use the image from DockerHub

`docker pull christinatao31/smart_meetings:app_server_v1`

`docker run -d -p 3000:3000 --name as christinatao31/smart_meetings:app_server_v1`

Navigate to <http://localhost:3000/>

#### Option 2: Build the Docker image

`docker image build -t christinatao31/smart_meetings:app_server_v1 .`

`docker container run -p 3000:3000 --name as christinatao31/smart_meetings:app_server_v1`

Navigate to <http://localhost:3000/>


### To remove the container

`docker container rm as`

### To remove the image

`docker images`

Find the image with the tag name `app_server_v1` and copy the `IMAGE ID`.

`docker image rm <IMAGE ID>`

### To run the container in the background, run

`docker run -d -p 3000:3000 --name as christinatao31/smart_meetings:app_server_v1`


