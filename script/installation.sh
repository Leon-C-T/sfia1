#!/bin/bash

source venv/bin/activate

python3 -m pip install flask

python3 -m pip install flask_mysqldb

source ~/.bashrc

python3 /var/lib/jenkins/workspace/sfia1/app.py