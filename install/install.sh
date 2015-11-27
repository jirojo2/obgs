#!/bin/bash

[ "$(id -u)" != "0" ] && echo "You must run this script as root" && exit 1

echo "Moving into frontend folder ..."
cd ../frontend/
echo "Installing npm if required ..."
apt-get install npm
echo "Installing bower ..."
npm install -g bower
echo "Installing ..."
npm install && bower --allow-root install
echo "Installing gulp ..."
npm install -g gulp
echo "Executing gulp ..."
gulp

