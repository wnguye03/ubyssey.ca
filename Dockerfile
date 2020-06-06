FROM python:3.8-buster
COPY . ./workspaces/ubyssey.ca/
WORKDIR /workspaces/ubyssey.ca/

# Config stuff
ENV DJANGO_SETTINGS_MODULE "config.settings.production"
ENV PORT 8000

# Installs some basics
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install curl

# Installs Node 14.x and npm 6.x
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Install the Django app's dependencies
RUN pip install -r requirements.txt

# Set up static files - clears old old version of node_modules that may be around, tides up new version
WORKDIR /workspaces/ubyssey.ca/ubyssey/static/
RUN rm -rf node_modules
RUN npm install
RUN npm install -g gulp
RUN npm audit fix
RUN npm rebuild node-sass
RUN gulp buildDev
RUN rm -rf node_modules

WORKDIR /workspaces/ubyssey.ca/
