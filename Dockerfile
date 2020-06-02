FROM python:3.8-buster
COPY . ./workspaces/ubyssey.ca/
WORKDIR /workspaces/ubyssey.ca/

# Installs some basics
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install curl

# Installs Node 14.x and npm 6.x
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Install the Django app's dependencies
RUN pip install -r requirements.txt

# Select settings. This is quickly going to be obselete
RUN cp _settings/settings-local.py ubyssey/settings.py


ENTRYPOINT ["sleep", "180"]



#WORKDIR /workspaces/ubyssey.ca/ubyssey/static/
#RUN rm -rf node_modules
#RUN npm install
#RUN npm install -g gulp
#RUN npm install -g gulp-cli
#RUN npm rebuild node-sass
#RUN gulp buildDev
#WORKDIR /workspaces/ubyssey.ca/
#RUN python manage.py migrate

#ENTRYPOINT ["/workspaces/ubyssey.ca/manage.py", "runserver", "0.0.0.0:8000"]