#!/bin/bash

source venv/bin/activate

pip3 install flask

python3 -m pip install flask_mysqldb

source ~/.bashrc

python3 app.py