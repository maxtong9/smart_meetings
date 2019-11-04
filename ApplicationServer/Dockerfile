# Ruby base image`
FROM ruby:2.6.5

WORKDIR /smart_meetings/application_server

# Install node, npm, yarn
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - \
 && apt-get install -yq nodejs

 # Install Ruby Gems, node modules, update yarn packages
COPY Gemfile Gemfile.lock package.json package-lock.json yarn.lock ./
RUN npm install \
 && npm install --global yarn \
 && bundle install \
 && yarn install --check-files

# Copy the rest of the files
COPY . .

# Run the application
EXPOSE 3000
RUN rails db:migrate RAILS_ENV=development
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-e", "development"]
