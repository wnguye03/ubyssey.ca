## Setup Instructions for Windows

Note that the following instructions are written based on using Git Shell (built on Windows Powershell). All the procedures have been tested when the instructions were published. 

Bash Sub-Linux system is still quite instable and would not be recommended (it does work though).

The steps for installing through Command Prompt should be identical, if not all the same. Please report any issues you have so that we would revise the instructions in the future.

You should install pip if you haven't already:


We recommend working inside a virtualenv, but it's not required.

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a new virtual environment
virtualenv ubyssey-dev
cd ubyssey-dev

# Activate the virtualenv
virtualenv activate```

Clone the `ubyssey-dispatch-theme` repository:

```bash
git clone https://github.com/ubyssey/ubyssey-dispatch-theme
cd ubyssey-dispatch-theme
```

Install the required Python packages with pip:

```bash
pip install -r requirements.txt
```

_Note: you might get an error saying that `libjpeg` is required. You can install it with Homebrew:_

```bash
```

Download the sample [project settings file](https://ubyssey.s3.amazonaws.com/dropbox/settings.py) and save it to `ubyssey-dispatch-theme/ubyssey/settings.py`.

### Database

Dispatch requires a MySQL database to store information. Install mysql with Homebrew. 

```bash
```

Now run the server and create a fresh database:

```bash

```

Next, populate the database with sample data:

```bash
curl https://ubyssey.s3.amazonaws.com/dropbox/ubyssey.sql | mysql -u root ubyssey
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

### Media Files

Download and unzip the [sample media folder](https://ubyssey.s3.amazonaws.com/dropbox/media.zip) to `ubyssey-dispatch-theme/media/`. This will make it so the images attached to the sample articles are viewable.

### Running the server

Now start the server!

```bash
python manage.py runserver
```

### Admin Panel

You can log in to the admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/):

__Email:__ volunteer@ubyssey.ca

__Password:__ volunteer
