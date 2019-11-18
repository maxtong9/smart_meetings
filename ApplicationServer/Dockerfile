# Ruby base image`
FROM ruby:2.6.5

WORKDIR /smart_meetings/application_server

# Install node, npm, yarn
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - \
 && apt-get install -yq nodejs \
 && npm install --global yarn

 # Install Ruby Gems, node modules, update yarn packages
COPY Gemfile package.json Gemfile.lock package-lock.json yarn.lock ./
RUN bundle install \
 && npm install

# Copy the rest of the files
COPY . ./
 
RUN yarn install --check-files
 
# # Run the application
EXPOSE 3000
# CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-e", "development"]
CMD ["rails", "server", "-b", "0.0.0.0"]
