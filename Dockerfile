# DOCKER-VERSION 0.0.1
FROM dockerfile/java
MAINTAINER Timothy Akampa timothyakampa@gmail.com

RUN apt-get -qq update
RUN apt-get -qqy install wget build-essential

# ---- Deploy mongo db server ----
RUN mkdir -p /data/db
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list
RUN apt-get -qq update
RUN apt-get install -y -q mongodb-org

# ---- Install Bower ----
RUN apt-get -qq update
RUN apt-get -qqy install nodejs
RUN apt-get -qqy install nodejs-legacy
RUN apt-get -qqy install npm
RUN npm install -g bower

# --- Install python, pip and virtualenv ----
RUN apt-get -qqy install python python-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN pip install virtualenv

# ---Add Django Core project ----
ADD . /necoc
RUN cd /necoc/dms/client/app && bower install --allow-root --quiet
RUN pip install -r /necoc/requirements.txt


# --- Add Ngnix and uWISG ---
RUN apt-get -qqy update && apt-get -qqy install nginx uwsgi uwsgi-plugin-python
ADD deployment/configs/necoc.conf  /etc/nginx/conf.d/necoc.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD deployment/configs/necoc-uwsgi.ini  /etc/uwsgi/apps-enabled/necoc-uwsgi.ini

# --- Add SSH for debugging ---
RUN apt-get update
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:root' |chpasswd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config


#--- Install Supervisord to run all background processes ---
RUN apt-get -qq update
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
RUN mkdir -p /var/log/mongodb
RUN mkdir -p /var/log/nginx
RUN mkdir -p /var/log/uwsgi
ADD deployment/configs/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

RUN mkdir -p /data/db
VOLUME ["/data", "/var/log/"]

# --- Add a starter script ----
ADD deployment/scripts  /scripts
RUN chmod +x /scripts/run.sh

# --- SSH ----
EXPOSE 22

# --- Nginx ---
EXPOSE 80 443 7999
CMD "/scripts/run.sh"