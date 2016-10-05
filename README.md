# Ubyssey Dispatch Theme

## Installation

We recommend working inside a virtualenv, but it's not required.

```bash
# Create a new folder for the virtual environment
virtualenv ubyssey-dev
cd ubyssey-dev

# Activate the virtualenv
source bin/activate
```

Clone the `ubyssey-dispatch-theme` repository:

```bash
git clone https://github.com/ubyssey/ubyssey-dispatch-theme
cd ubyssey-dispatch-theme
```

Install the required Python packages with pip:

```bash
pip install -r requirements.txt
```

Download the sample [project settings file](https://ubyssey.s3.amazonaws.com/settings.py) and save it to `ubyssey-dispatch-theme/ubyssey/settings.py`.

### Database

Dispatch requires a MySQL database to store information. If you're using a Mac, install mysql with Homebrew. 

If you don't have Homebrew installed, run this command:

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Install mysql:

```bash
brew install mysql
```

### Static files

Install the required Node packages with npm:

```bash
cd ubyssey/static
npm install
```

Install a global verison of gulp (if you don't have it already) and build the static files:

```bash
npm install -g gulp
gulp
```

### Running the server

Before starting the server, run `createsuperuser` to make yourself an account for the admin panel:

```bash
python manage.py createsuperuser
```

Now start the server!

```bash
python manage.py runserver
```


