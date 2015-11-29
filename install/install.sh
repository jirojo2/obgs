#!/bin/bash

[ "$(id -u)" != "0" ] && echo "You must run this script as root" && exit 1


echo "Moving into frontend folder ..."
cd ../frontend/

[ -d node_modules ] && echo "Cleaning installation folder ..." && rm -fr node_modules
echo "Checking if npm is installed ..."
type npm > /dev/null
if [[ $? -eq 0 ]]
then
	echo "npm is installed ..."
else
	if [[ $(grep -c -i debian /proc/version) -gt 0 || $(grep -c -i ubuntu /proc/version) -gt 0 ]]
	then
		echo "Debian/Ubuntu installation detected ..."
		read -p "Do you want to automatically install dependencies?" -n 1 -r
		if [[ $REPLY =~ ^[Yy]$ ]]
		then
        		apt-get -qq install npm
		fi
	else
		echo "Please install npm before continuing."
		exit 1
	fi
fi

echo "Checking if nginx is installed ..."
type nginx > /dev/null
if [[ $? -eq 0 ]]
then
        echo "nginx is installed ..."
else
        if [[ $(grep -c -i debian /proc/version) -gt 0 || $(grep -c -i ubuntu /proc/version) -gt 0 ]]
        then
                echo "Debian/Ubuntu installation detected ..."
                read -p "Do you want to automatically install dependencies?" -n 1 -r
                if [[ $REPLY =~ ^[Yy]$ ]]
                then
                        apt-get -qq install nginx
                fi
        else
                echo "Please install nginx before continuing."
                exit 1
        fi
fi


echo "Fetching masscan from git ..."
git clone https://github.com/robertdavidgraham/masscan
echo "Building masscan ..."
cd masscan
make
[[ $? != 0 ]] && echo "Error compiling masscan, please check." && exit 1
echo "Installing masscan ..."
make install
echo "Cleaning up ..."
rm -fr masscan

echo "Checking if mongo-server is installed ..."
type mongod > /dev/null
if [[ $? -eq 0 ]]
then
        echo "mongo-server is installed ..."
else
        if [[ $(grep -c -i debian /proc/version) -gt 0 || $(grep -c -i ubuntu /proc/version) -gt$
        then
                echo "Debian/Ubuntu installation detected ..."
                read -p "Do you want to automatically install dependencies?" -n 1 -r
                if [[ $REPLY =~ ^[Yy]$ ]]
                then
                        apt-get -qq install mongo-server
                fi
        else
                echo "Please install mongo-server before continuing."
                exit 1
        fi
fi

echo "Installing bower ..."
npm --silent install -g bower

echo "Installing ..."
npm --silent install && bower --silent --allow-root install

echo "Installing gulp ..."
npm --silent install -g gulp

echo "Executing gulp ..."
gulp

echo "Checking if systemctl is avaliable ..."
type systemctl

if [[ $? -eq 0 ]]
then
	echo "Configuring obgs systemctl files ..."
	sed -i -e 's/ExecStart=\/srv\/obgs\/farmer\/farmer.py/ExecStart=`pwd`/farmer/farmer.py/g' install/obgs-farmer.service
	sed -i -e 's/ExecStart=\/srv\/obgs\/farmer\/server.py/ExecStart=`pwd`/farmer/server.py/g' install/obgs-api.service
	echo "Installing obgs services for systemctl ..."
	cp install/obgs-farmer.service /etc/systemd/system/
	cp install/obgs-api.service /etc/systemd/system/
	systemctl daemon-reload
	read -p "Do you want to automatically start the services?" -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
		systemctl start obgs-farmer.service obgs-api.service
        fi

else
	echo "systemctl not found ..."
fi

