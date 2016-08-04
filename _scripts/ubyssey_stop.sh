#!/bin/bash

# Stop the server
if [ -f run/ubyssey.pid ]; then
  sudo kill `cat run/ubyssey.pid`
fi
