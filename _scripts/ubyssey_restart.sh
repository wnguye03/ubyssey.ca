#!/bin/bash

UBYSSEY_APP_DIR=/var/webapps/ubyssey
GUNICORN_SCRIPT=/var/webapps/ubyssey/_scripts/gunicorn_start.sh

# Set permissions on gunicorn start script
sudo chown ubyssey $GUNICORN_SCRIPT
sudo chmod u+x $GUNICORN_SCRIPT

# Activate the virtual environment
cd $UBYSSEY_APP_DIR
source bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static and upload to S3
python manage.py collectstatic --no-input

# Restart gunicorn
sudo supervisorctl restart ubyssey
