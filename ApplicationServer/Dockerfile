FROM ruby:2.6.5
COPY . /smart_meetings/application_server
WORKDIR /smart_meetings/application_server

# install node, npm, yarn
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - \
 && apt-get install -yq nodejs

 # install Ruby Gems, node modules, update yarn packages
RUN bundle install \
 && npm install \
 && npm install --global yarn \
 && yarn install --check-files

# run the application
EXPOSE 3000
RUN rails db:migrate RAILS_ENV=development
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-e", "development"]
