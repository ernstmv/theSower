#! /bin/bash

if [ -f /etc/os-release ]; then
  . /etc/os-release
else
  echo "Cannot find /etc/os-release. Please proced manually"
fi

case $ID in
  arch)
    echo "You are cool"
    sudo pacman -S --noconfirm python3 tk
    ;;
  ubuntu)
    sudo apt install -y python3 python3-tk
    ;;
  fedora)
    sudo dnf install -y python3 python3-tkinter
    ;;
  *)
    echo "Distro not recognized, please add support to your distro in this script and send PR"
    exit 1
    ;;
esac
exit 0


CURRENT_PATH=$(pwd)

echo "[1/3] Creating virtual enviorment at $CURRENT_PATH"
python3 -m venv virtualenv

if [ $? -ne 0 ]; then
  echo "ERROR: Unable to create virtual enviorment. Check your python3 installation"
  exit 1
fi

echo "Virtual enviorment created"

echo "[2/3] Activating virtual enviorment"
. virtualenv/bin/activate

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

echo "Libraries installed, you are done folk"
