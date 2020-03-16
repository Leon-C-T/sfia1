#!/bin/bash

source venv/bin/activate

sudo python3 -m pip install flask

sudo python3 -m pip install flask_mysqldb

source ~/.bashrc

python3 app.py