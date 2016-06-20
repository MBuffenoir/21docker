# 21 Docker

## Requirements

Have docker toolbox installed and cs configured to call Exoscale API.

## Create a docker machine to host containers

    docker-machine create --driver exoscale \
        --exoscale-api-key $CLOUDSTACK_KEY \
        --exoscale-api-secret-key $CLOUDSTACK_SECRET_KEY \
        --exoscale-instance-profile small \
        --exoscale-disk-size 10 \
        --exoscale-security-group 21docker \
        21host

    eval $(docker-machine env 21host)

# Run the application using docker and compose

Copy files and ssh to the host:
    
    docker-machine scp -r . 21host:
    docker-machine ssh 21host

Make sure compose is installed on your host:

    curl -L https://github.com/docker/compose/releases/download/1.7.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

<!-- Start a redis server on your host with:

    docker run --name redis -p 127.0.0.1:6379:6379 -d redis redis-server --appendonly yes -->

Add current user to group ubuntu

    sudo gpasswd -a ${USER} docker

<!-- Run the following commands:

    sudo apt-get update
    curl https://21.co | sh
    sudo apt-get -y install python-dev
    sudo apt-get remove python-pip
    sudo easy_install-3.4 pip
    sudo pip install -r requirements.txt -->

Setup 21 on the host

    21 login

Build, then run the web server with:

    docker-compose up -d
<!-- 
Open a second terminal, connect to 21host and run the worker with:

    celery -A worker worker -B --loglevel=INFO -->

The worker will remove all expired containers after 10 minutes.

## 21 buy

Run an offchain payment to test with:

    21 buy \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -X POST \
        -d '{"image":"nginx:latest","ports":[80,443]}' \
        http://$(docker-machine ip 21host):5000/docker/run/

To define udp port use: ``"ports":[(53, 'udp'), 5000]} -> To be battle tested ...

## TODO

Dockerfile for project. 

    docker run -v /var/run/docker.sock:/var/run/docker.sock

Be sure to update your manifest file your 21co ip address

Repay to add some time to your container (payment channel ?)

Add environments variable, volumes etc ...

Support swarm

Support load-balancing with Traeffik

Time left endpoint
