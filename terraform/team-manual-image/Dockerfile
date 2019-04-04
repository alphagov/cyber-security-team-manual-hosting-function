FROM ruby:2.6.2
RUN apt-get update -y && \
apt-get install -y nodejs
ADD cyber-security-team-manual-gemfile-git/Gemfile ./
ADD cyber-security-team-manual-gemfile-git/Gemfile.lock ./
RUN bundle install
