#!/bin/bash

# Start the server
sudo -u ubyssey -H sh -c "${BASH_SOURCE%/*}/gunicorn_start"
