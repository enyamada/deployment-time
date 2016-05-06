#!bin/bash
# 
# Scheduler deployment script.
# In a nutshell, it ensures docker is installed and running and then runs 2 containers (one with a mysql
# server, another with the scheduler server).
#

mkdir api

cat > api/docker-compose.yml <<EOL
version: '2'
services:
  fe:
    image: enyamada/steps-fe:1.0
    ports:
     - "80:5000"
    volumes:
     - /var/log:/var/log
    networks:
     - elo7
    depends_on:
     - db
    environment:
     - DB_HOST=db
     - LOG_LEVEL=debug
  db:
    image: enyamada/steps-db:1.0
    volumes:
     - /var/lib/mysql:/var/lib/mysql
    networks:
     elo7:
       aliases:
         - db
    environment:
     - MYSQL_ROOT_PASSWORD=Sdahlkj7%a



networks:
    elo7:
      driver: bridge
EOL

cat > /etc/yum.repos.d/docker.repo <<EOL
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOL



touch /tmp/start

# Install & start docker
yum update -y
yum install docker-engine -y
service docker start

# Install docker-compose
curl -L https://github.com/docker/compose/releases/download/1.7.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Starts up docker compose
cd api
/usr/local/bin/docker-compose up -d

touch /tmp/fin

