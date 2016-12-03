#!/bin/sh

#Start green unicorn
echo "Starting the OpenODS service"
cd /openods

ls -lrt /openods/

exec gunicorn -b 0.0.0.0:8080 -w 4 app:app
#exec /home/py3env/bin/gunicorn -b 0.0.0.0:8080 -w 4 app:app
#python run.py

