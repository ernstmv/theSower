#! /bin/bash

CURRENT_PATH=$(pwd)

echo "[1/3] Creating virtual enviorment at $CURRENT_PATH"
python3 -m venv virtualenv

if [ $? -ne 0 ]; then
  echo "ERROR: Unable to create virtual enviorment. Check your python3 installation"
  exit 1
fi

echo "Virtual enviorment created"

echo "[2/3] Activating virtual enviorment"
source virtualenv/bin/activate

if [ $? -ne 0 ]; then
  echo "ERROR: Cannot activate the virtual enviorment, Make sure your shell is neither bash or zsh"
  exit 1
fi

echo "Virtual enviorment activated"

echo "[3/3] installing required libraries" 
pip install opencv-python matplotlib pillow customtkinter pyserial pyudev  
if [ $? -ne 0 ]; then
  echo "ERROR: Can't install the required libraries, check your python version"
  exit 1
fi

echo "Libraries installed"
