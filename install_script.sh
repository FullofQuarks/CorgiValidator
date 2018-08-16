#!/bin/bash

# install web server dependencies
sudo apt-get update
sudo apt-get install python python-virtualenv nginx supervisor -y

# install application (source location in $1)
mkdir /home/vagrant
mkdir /home/vagrant/login
cp -R $1/login/* /home/vagrant/login/

# create a virtualenv and install dependencies
virtualenv /home/vagrant/login/venv
/home/vagrant/login/venv/bin/pip install -r /home/vagrant/login/requirements.txt

# configure supervisor
sudo cp /vagrant/login.conf /etc/supervisor/conf.d/
sudo useradd -M vagrant
sudo mkdir /var/log/login
sudo supervisorctl reread
sudo supervisorctl update

# configure nginx
sudo cp /vagrant/login.nginx /etc/nginx/sites-available/login
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/login /etc/nginx/sites-enabled/
sudo service nginx restart

echo Application deployed to http://192.168.33.10/
