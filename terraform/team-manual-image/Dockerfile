FROM ruby:2.6.2
RUN apt-get update -y && \
apt-get install -y nodejs
COPY cyber-security-team-manual-gemfile-git/Gemfile cyber-security-team-manual-gemfile-git/Gemfile.lock ./
RUN bundle install
