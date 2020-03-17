#!/bin/bash

source venv/bin/activate

sudo su jenkins

python3 -m pip install flask

python3 -m pip install flask_mysqldb

python3 -m pip install pytest

python3 -m pip install urllib3

python3 -m pip install pytest-base-url

python3 -m pip install coverage

source ~/.bashrc

python3 /var/lib/jenkins/workspace/sfia1/app.py