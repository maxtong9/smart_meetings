# Ruby base image`
FROM ruby:2.6.5

WORKDIR /smart_meetings/application_server

# Install node, npm, yarn
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - \
 && apt-get update -qq \
 && apt-get install -yq nodejs \
 && npm install --global yarn

 # Install Ruby Gems using bundle, node modules using yarn, update yarn packages
COPY Gemfile package.json Gemfile.lock yarn.lock ./
RUN bundle install
#  && npm install \
RUN yarn install --check-files

# COPY entrypoint.sh /usr/bin/
# RUN chmod +x /usr/bin/entrypoint.sh
# ENTRYPOINT ["entrypoint.sh"]

# Copy the rest of the files
COPY . ./
 
# RUN yarn install --check-files
 
# Run the application
EXPOSE 3000
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
# CMD ["rails", "server", "-b", "0.0.0.0"]
# CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-e", "development"]
