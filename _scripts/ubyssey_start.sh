#!/bin/bash

GUNICORN_SCRIPT=/var/webapps/ubyssey/_scripts/gunicorn_start.sh

# Start the server
sudo chown ubyssey $GUNICORN_SCRIPT
sudo chmod u+x $GUNICORN_SCRIPT

sudo supervisorctl start ubyssey
