OBGS - Open Banner Grabbing System
==================================

# Installation

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

# Frontend

Use `gulp` to compile the frontend, and setup apache/nginx
to serve the `public` folder (see wiki for config examples)

```bash
$ cd frontend
$ npm install
$ bower install
$ gulp
```

# API

Run `server.py`, until a proper service method (systemd) is prepared.

Edit `settings.py` to match the MongoDB settings and the data schema.

# Farmer

Run `farmer.py` module, until a proper service method (systemd) is prepared.

