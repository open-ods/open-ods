#!/bin/sh

# Start OpenODS using GreenUnicorn WSGI server
echo "Starting the OpenODS service"
cd /openods

exec gunicorn -b 0.0.0.0:8080 -w 4 openods:app