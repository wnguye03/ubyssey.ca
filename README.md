# Ubyssey Dispatch Theme

## Installation

[Docker Instructions](/SETUP_DOCKER.md)

[Mac Instructions](https://code.ubyssey.ca/getting-started/installation/mac.html)

[Windows Instructions](https://code.ubyssey.ca/getting-started/installation/windows.html)

## Development

Once you have your local environment configured, follow these steps to start the server for development:

### New way with Docker
  navigate to your ubyssey-dev directory.
  ```bash
    docker-compose up
  ```
  If on linux you may need to run the above command with sudo
  
  That should be it, happy hacking!
  
### Old way without Docker

#### Mac OSX

```bash
# Start the MySQL server
mysql.server start

# If that doesn't work, try:
brew services start mysql

# Activate your virtualenv (if you're using one)
cd ubyssey-dev
source bin/activate

# Run the server!
cd ubyssey.ca
python manage.py runserver

# In a separate terminal tab, start the gulp process. It will watch for changes to the source files and automatically re-build the static files during development.
cd ubyssey.ca/ubyssey/static/
gulp
```

#### Windows

First, make sure your MySQL server is running!

```bash

# Activate your virtualenv (if you're using one)
cd ubyssey-dev
.\Scripts\activate

# Run the server!
cd ubyssey.ca
python manage.py runserver

# In a separate command prompt window, start the gulp process. It will watch for changes to the source files and automatically re-build the static files during development.
cd ubyssey.ca/ubyssey/static/
gulp
```

## Office hours

Our office hours for 2018 is 12:30 - 2:00 every Thursday.
