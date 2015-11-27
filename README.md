OBGS - Open Banner Grabbing System
==================================

# Installation

First, install dependencies:

```bash
$ sudo pip install eve
$ sudo pip install pymongo
```

# Frontend

Use `gulp` to compile the frontend, and setup apache/nginx
to serve the `public` folder (see wiki for config examples)

```bash
$ cd frontend
$ gulp
```

# API

Run `server.py`, until a proper service method (systemd) is prepared.

Edit `settings.py` to match the MongoDB settings and the data schema.

# Farmer

Run `farmer.py` module, until a proper service method (systemd) is prepared.

