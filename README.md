OBGS - Open Banner Grabbing System
==================================

# Installation

##Automatic installation

There is an script under the folder install.sh that will install OBGS and its dependencies with a configuration by default.

WARNING: This script is still under development so use it at your own risk!

##Manual installation

First, install dependencies. For example, with a debian based system:

```bash
$ sudo apt-get install npm nodejs-legacy mongodb-server
$ sudo pip install eve
$ sudo npm install -g bower gulp
```

Then, we need to install [masscan](https://github.com/robertdavidgraham/masscan)

```
$ sudo apt-get install git gcc make libpcap-dev
$ git clone https://github.com/robertdavidgraham/masscan
$ cd masscan
$ make
$ sudo make install
```
Reference masscan's readme for further instructions.

When deploying in a server, if `systemd` is available:
```
$ sudo cp install/obgs-farmer.service /etc/systemd/system/
$ sudo cp install/obgs-api.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl start obgs-farmer.service obgs-api.service
```

### Frontend

Use `gulp` to compile the frontend, and setup apache/nginx
to serve the `public` folder (see wiki for config examples)

```bash
$ cd frontend
$ npm install
$ bower install
$ gulp
```

### API

Edit `settings.py` to match the MongoDB settings and the data schema.

Use systemd service to control the api service, or run manually `api/server.py`.

### Farmer

Use systemd service to control the farmer service, or run manually `farmer/farmer.py`.

