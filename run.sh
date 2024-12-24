#!/bin/bash

if [ ! -d "venv" ]; then
    python -m venv venv
fi

source venv/bin/activate;

pip install --no-warn-script-location -r requirements.txt;

python main.py