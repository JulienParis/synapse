


## **synapse** is a web application based on [Flask](http://flask.pocoo.org/) Python microframework, mongoDB database, Zeep, mySQL, and Three.js
## **synapse** is available online for now at : **[synapse.la-bibliotheque.com](http://synapse.la-bibliotheque.com)**.


----------------------------------------------------
## Licence & copyrights :

- **Licence** : [GNU](https://github.com/JulienParis/synapse/blob/master/LICENSE)

- **Project by** : [Julien Paris](http://jpylab.com/)

- **Author code** : Copyright (C) 2017 [Julien Paris](http://jpylab.com/)

- **Contact** : [youremail@email.com](mailto:youremail@email.com)


>
Copyright (C) 2017  Julien PARIS
>


-----------------------------------------------------
## Features :

This application proposes several features :


-----------------------------------------------------
# _DOCUMENTATION_ :

## _REQUIREMENTS_ | Application requirements :

  - Python 2.7
  - MongoDB
  - Python libraries : Pandas, flask-socketio, eventlet, zeep, flask-mysqldb
  - NGINX
  - Gunicorn
  - server side : ubuntu 16.04


---

## _LOCAL SETTINGS_ | Installation on a local machine :


  > mysql use (temporary) : https://stackoverflow.com/questions/8195418/cant-access-mysql-from-command-line-mac
  ```
  $ export PATH=$PATH:/usr/local/mysql/bin
  ```

  >
  ```
  $ git config --global user.name 'your_username'
  $ git config --global user.email ‘youremail@email.com’
  ```

  - clone synapse project from github :
  >
  ```
  $ git clone https://github.com/JulienParis/synapse.git

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



## _SERVER_CONFIGURATION_ | Installation on Ubuntu server (after SSH access):

  - connect to server : `$ ssh your_username@xx.xx.xxx.xx`

  - update ubuntu : `$ sudo apt-get update`

  - configure server firewall for socketIO (port 5000), NGINX/Gunicorn (port 8000, www) :
  >
  ```
  $ sudo ufw allow www
  $ sudo ufw allow http
  $ sudo ufw allow 8000
  $ sudo ufw allow 5000
  $ sudo ufw allow 22
  $ sudo ufw allow 443
  $ sudo ufw enable
  $ sudo apt-get update
  $ sudo apt-get install ntp
  ```

  - *** if needed: `$ sudo ufw delete allow 80`

  - check enabled ports : `$ sudo ufw show added`



## _MONGODB_ | MongoDB installation :

  - check installation procedure on  :
  <https://docs.mongodb.com/manual/installation/>
  <https://docs.mongodb.com/manual/administration/install-on-linux/>
  <https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/>

  - Import the public key used by the package management system
  >
  ```
  $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
  ```

  - create a list file for mongodb (Ubuntu 16.04)
  >
  ```
  $ echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
  ```

  - install mongodb>
  >
  ```
  $ sudo apt-get update
  $ sudo apt-get install -y mongodb-org
  ```

  - create `~/data/db` and authorize in read-write (on Ubuntu)
  - cf : <https://stackoverflow.com/questions/7948789/mongodb-mongod-complains-that-there-is-no-data-db-folder>
  >
  ```
  $ sudo mkdir -p /data/db
  $ grep mongo /etc/passwd
  --> mongodb:x:_123_:_456_::/home/mongodb:/bin/false
  $ sudo chmod 0755 /data/db
  $ sudo chown -R _123_:_456_ /data/db
  $ sudo chown -R `id -u` /data/db
  ```

  - *** start mongo shell (optional) / test mongo once data/db created : `$ mongod`

  - start mongodb : `$ sudo service mongod start`
  - stop  mongodb : `$ sudo service mongod stop`



## _GIT integration + SSH_ on Ubuntu server ****

  - cf : <https://www.youtube.com/watch?v=OtxdNuodlIE>
  - cf : <https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-16-04>

  - connect to server : `—> your_username@xx.xx.xxx.xx $`

  - ** if not set yet : create SSH key
  >
  ```
  $ ssh-keygen -t rsa -C "youremail@email.com" -b 4096
  or
  $ ssh-keygen -t rsa -b 4096
  (save it to /root/.ssh/id_rsa +Y )
  (empty passphrase + Y )
  ```

  - ** check if ssh-agent enabled
  >
  ```
  $ eval "$(ssh-agent -s)"
  --> Agent pid 1234
  ```

  - add identity :
  >
  ```
  $ ssh-add ~/.ssh/id_rsa
  $ cat ~/.ssh/id_rsa.pub
  (copy ssh key)
  ```

  - add .ssh / config  :
  - cf : <https://about.gitlab.com/2016/02/18/gitlab-dot-com-now-supports-an-alternate-git-plus-ssh-port/>
  >
  ```
  $ sudo vi ~/.ssh/config
  (copy paste + ESC + :WQ + enter)
  Host gitlab.com
    Hostname altssh.gitlab.com
    User git
    Port 443
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa
  ```

  - go to gitlab / github (on gitlab : https://gitlab.com/profile/keys) : `--> add ssh key to authorized keys / deployment keys`

  - back to server - ssh : `—> your_username@xx.xx.xxx.xx:$ ...`

  - install GIT on the server : `$ sudo apt-get install git`

  - config GIT :
  >
  ```
  $ git config --global user.name 'yourname'
  $ git config --global user.email ‘youremail@email.com’
  ```

  - create a directory to store apps : `$ sudo mkdir apps`

  - go to home/apps + add project
  >
  ```
  $ cd apps
  $ git config --list
  $ git init
  $ git remote add origin https://github.com/JulienParis/synapse.git
  ```

  - and clone :
  >
  ```
  $ git clone git@github.com/JulienParis/synapse.git
  $ ...
  $ git remote -v
  ```

  - check if files were copied with a simple `$ ls`

  - also see : <https://www.youtube.com/watch?v=swMJHoo1IBI>



## _FW_NGINX_ on Ubuntu server ****


  - install NGINX on the server : cf <https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-16-04>
  >
  ```
  $ sudo apt-get install nginx
  $ service nginx restart
  $ sudo ufw app list
  $ sudo ufw allow 'Nginx Full
  $ sudo ufw status
  ```

  - check web server : `$ systemctl status nginx`
  >
  ```
  $ sudo apt-get install curl
  $ curl -4 icanhazip.com
  ```

  - install Python, PIP, and dependencies :
  >
  ```
  $ sudo apt-get install python-pip python-dev
  $ sudo apt-get install libmysqlclient-dev
  $ sudo apt-get install libssl-dev ---> for cryptography
  $ sudo apt-get install python-mysqldb
  $ pip install -r requirements.txt
  $ pip install gunicorn
  $ pip install eventlet
  ```

  - configure NGINX (reroute port 5000 to root) :
  >
  ```
  $ cd ~/etc/nginx/sites-enabled
  ```

  - create NGINX configuration file for synapse
  >
  ```
  $ sudo vi synapse
  ESC + i
  ```

  - copy/paste NGINX configuration settings
  >
  ```
  	# configuration containing list of application servers
  	upstream app_server {
  	  server 0.0.0.0:5000 fail_timeout=0;
  	}
  	# configuration for Nginx
  	server {
  	  # running port
  	  listen 80 default_server ;
  	  server_name synapse.la-bibliotheque.com ;
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

  - save `synapse` NGINX config file : `ESC + :wq + ENTER`


  - remove default nginx file from `/etc/nginx/sites-enabled`
  >
  ```
  $ sudo rm default
  ```

  - test for syntax errors by typing : `$ sudo nginx -t`

  - restart the NGINX process to read the our new config : `$ sudo service nginx restart`


  - DNS settings : https://askubuntu.com/questions/346838/how-do-i-configure-my-dns-settings-in-ubuntu-server
  >
  ```
  $ cd ~/etc/networks
  $ sudo nano interfaces
  ...
  dns-nameservers ... 80.82.225.40
  ...
  $ sudo ifdown eth0 && sudo ifup eth0
  ```
  
  > edit etc/hosts --> https://www.imore.com/how-edit-your-macs-hosts-file-and-why-you-would-want
  > add IP to redirect 

  - copy original config.py file to server (from local machine)
  - cf : <https://unix.stackexchange.com/questions/106480/how-to-copy-files-from-one-machine-to-another-using-ssh>
  >
  ```
  $ scp /Users/username/PATH/TO/PROJECT/config.py your_username@xx.xx.xxx.xx:/home/julien/apps/synapse
  ```

  - GIT maintainance : pull when changes
  >
  ```
  $ ssh your_username@xx.xx.xxx.xx    ... + pwd
  $ cd apps/synapse
  $ git pull
  ```

  - run application : go to same level than `wsgi.py` and start app with Gunicorn
  - cf : https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04
  - cf : http://docs.gunicorn.org/en/stable/settings.html#raw-env 
  >
  ```
  $ cd apps/synapse
  // deprecated // $ gunicorn --bind=0.0.0.0:5000 —-timeout=120 --workers=1 —-worker-class=eventlet wsgi:app &
  $ gunicorn -b 0.0.0.0:5000 -k eventlet -t 120 -w 1  wsgi:app
  ```

  - ( if needed / stop gunicorn server ) : `$ pkill gunicorn`
