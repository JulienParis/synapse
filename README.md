


## **synapse** is a web application based on [Flask](http://flask.pocoo.org/) Python microframework and Three.js
## **synapse** is not available online for now : **[synapse.fr]()**.


----------------------------------------------------
## Licence & copyrights :

- **Licence** : [???]()

- **Project by** : [Julien Paris](http://jpylab.com/)

- **Author code** : Copyright (C) 2017 [Julien Paris](http://jpylab.com/)

- **Contact** : [jparis.py@gmail.com](mailto:jparis.py@gmail.com)


>
Copyright (C) 2017  Julien PARIS
>
Also add information on how to contact you by electronic and paper mail.


-----------------------------------------------------
## Features :

This application proposes several features :


-----------------------------------------------------
# Installation documentation :

## Application requirements :

- Python 2.7
- Python libraries : Pandas, flask-socketio, eventlet, Pandas3D, Numpy-stl
- NGINX
- Gunicorn
- server side : ubuntu 14.04 x64 | 4 Go RAM minimum

---

## _A._ | Installation on a local machine :

- clone synapse project from gitlab :
>
```
$ git clone git@gitlab.com:Julien_P/synapse.git
```

- install, create and activate a virtual environment :
>
```
$ pip install virtualenv
$ sudo virtualenv venv
$ source venv/bin/activate
```

- install Python dependencies (Flask, pandas, etc...) within the virtual environment:
>
```
(venv)$ pip install -r requirements.txt
```

- run synapse in debugging mode :
>
```
(venv)$ python run_synapse.py
```

- in browser open the following address : `http://127.0.0.1:5000`

---

## _B._ | Installation on Ubuntu server (after SSH access):

- update ubuntu : `$ sudo apt-get update`

- install GIT on the server : `$ sudo apt-get install git`

- clone synapse project from gitlab :
>
```
$ mkdir apps
$ cd app
$ git config --list
$ git init
$ git clone git@gitlab.com:Julien_P/synapse.git
```

- configure your server SSH...

- configure server firewall for socketIO (port 5000), NGINX/Gunicorn (port 8000, www) :
>
```
$ sudo ufw allow www
$ sudo ufw allow 8000
$ sudo ufw allow 5000
$ sudo ufw enable
$ sudo apt-get update
$ sudo apt-get install ntp
```

- install NGINX on the server :
>
```
$ sudo apt-get install nginx
$ service nginx restart
```

- install Python, PIP, and dependencies :
>
```
$ sudo apt-get install python-pip python-dev
$ pip install -r requirements.txt
$ pip install gunicorn
$ pip install eventlet
```

- configure NGINX (reroute port 5000 to root) :
>
```
$ cd ~/etc/nginx/sites-enabled`
```
create NGINX configuration file for synapse
```
$ sudo vi synapse
ESC + i
```
copy/paste NGINX configuration settings
```
	# configuration containing list of application servers
	upstream app_server {
	  server 0.0.0.0:5000 fail_timeout=0;
	}
	# configuration for Nginx
	server {
	  # running port
	  listen 80 default_server ;
	  server_name synapse.com ;
	  # Proxy connection to the application servers
	  location / {
	    proxy_pass http://app_server ;
	    proxy_redirect off ;
	    proxy_set_header Host $http_host;
	    proxy_set_header X-Real-IP $remote_addr;
	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	    proxy_set_header X-Forwarded-Host $server_name;
	  }
	}
```
save `synapse` NGINX config file
```
ESC + :wq + ENTER
```
test for syntax errors by typing:
```
$ sudo nginx -t
```
restart the NGINX process to read the our new config:
```
$ sudo service nginx restart
```

- run application : go to same level than `wsgi.py` and start app with Gunicorn
>
```
$ cd apps/synapse
$ gunicorn --bind 0.0.0.0:5000 —-timeout=120 --workers=1 —-worker-class eventlet wsgi:app &
```

- ( if needed / stop unicorn server ) : `$ pkill gunicorn`
