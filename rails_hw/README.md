# README
MacOS setup:

##Installing Homebrew
First, we need to install Homebrew. Homebrew allows us to install and compile software packages easily from source.

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

##Install Ruby version 2.6.5

To do this, run the following commands in your Terminal:

`brew install rbenv ruby-build

# Add rbenv to bash so that it loads every time you open a terminal
echo 'if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi' >> ~/.bash_profile
source ~/.bash_profile

# Install Ruby
rbenv install 2.6.5
rbenv global 2.6.5
ruby -v`

##Install Rails version 6.0.0

`gem install rails -v 6.0.0`

`rbenv rehash`

Check version:

`rails -v
# Rails 6.0.0`

##Install Nodejs version 13.0.0

`brew install node`

Check node version and npm version

`node -v

npm -v`

##Install Gems in Gemfile

`bundle install`

##Install node_modules folder

`npm install`

##Install yarn

`brew install yarn`

Update Yarn packages

`yarn install --check-files`

Open two terminals in the rails_hw directory

run:

`rails s`

Then locate to localhost:

On the second window run (Ignore if not making direct changes to application):

`bin/webpack-dev-server`
