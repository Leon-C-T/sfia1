#!/bin/bash
source ~/.bashrc
pip3 show coverage
python3 -m coverage run -m pytest /var/lib/jenkins/workspace/sfia1/test/testing.py
python3 -m coverage report -m