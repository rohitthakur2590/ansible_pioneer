#!/bin/sh
# install dependencies
pip install -r requirements.txt
#
# run the server
#
cd app
python app.py
