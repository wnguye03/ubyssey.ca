#!/bin/bash

# Start the server
sudo chown ubyssey ${BASH_SOURCE%/*}/gunicorn_start
sudo chmod u+x ${BASH_SOURCE%/*}/gunicorn_start
sudo -u ubyssey -H sh -c "${BASH_SOURCE%/*}/gunicorn_start"
