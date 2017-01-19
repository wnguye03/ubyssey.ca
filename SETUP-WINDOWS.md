## Setup Instructions for Windows

Note that the following instructions are written based on using Git Shell (built on Windows Powershell). All the procedures have been tested when the instructions were published. 

Bash Sub-Linux system is still quite instable and would not be recommended (it does work though, and you can follow the Mac instructions).

The steps for installing through Command Prompt should be identical, if not all the same. Please report any issues you have so that we would revise the instructions in the future.

Note that this is the very first edition for the back-end set up on Windows machines, expect to see flux and inaccuracies in content.

You should install Python if you haven't already:
```bash
https://www.python.org/downloads/
```

You should install pip if you haven't already, note that pip usually comes with the installation of python. If you do not have pip installed, following the instructions here: https://pip.pypa.io/en/stable/installing/


We recommend working inside a virtualenv, but it's not required.

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a new virtual environment
virtualenv ubyssey-dev
cd ubyssey-dev

# Activate the virtualenv
.\Scripts\activate
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

_Note: you might get an error saying that `_mysql.c(42) : fatal error C1083: Cannot open include file: 'config-win.h': No such file or directory`. To resolve this issue

```bash
pip install wheel

download from http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python

Choose the one that is corresponding to the edition of your Python (32-bit or 64-bit). Occacionally, things get complicated if you install 32-bit python on 64-bit system, if that's the case, you could try both of them.
```

Download the sample [project settings file](https://ubyssey.s3.amazonaws.com/dropbox/settings.py) and save it to `ubyssey-dispatch-theme/ubyssey/settings.py`.

### Database

Dispatch requires a MySQL database to store information. Install mysql with mysql Installer.

```bash
https://dev.mysql.com/downloads/windows/installer/5.6.html
```

You can set a password for root user, if you do, you will need to change the attribute of password in the setting.py file that you previously downloaded.

Now run the MySQL command line client that comes with mysql installation and create a fresh database:

```bash
CREATE DATABASE ubyssey
```

Next, save the sample data from https://ubyssey.s3.amazonaws.com/dropbox/ubyssey.sql to local drives
and load the data file to the database.

```bash
USE ubyssey
source ubyssey.sql
```

### Static files

Install the required Node packages with npm from the following link:

```bash
https://nodejs.org/en/
```

To check if npm and node are successfully installed, in your command line, type:

```bash
npm -v
node -v
```

Install a global verison of gulp (if you don't have it already) and build the static files:

```bash
cd ubyssey\static
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
