# 21 Docker

## Requirements

Have docker toolbox installed and cs configured if you want to use Exoscale compute API to create your hosting instance.
You can of course use any other provider that docker-machine supports to host the project.

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

    sudo su
    curl -L https://github.com/docker/compose/releases/download/1.7.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x usr/local/bin/docker-compose

Add current user to group ubuntu

    sudo gpasswd -a ${USER} docker

Install 21 on the host to facilitate account management:

    curl https://21.co | sh

Setup 21 on the host (In particular this will connect your host to the 21 private network and create proper configuration file in a .two1 folder. We can then mount this folder in our app using docker.):

    21 login

Be sure to update your manifest file with your 21co ip address.

Build, then run the web server with:

    docker-compose up -d

The worker container will remove all expired containers after 10 minutes.

## Tests

Run the tests with:

    docker-compose exec 21docker python -m unittest discover

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

Repay to add some time to your container (payment channel ?)

Support swarm

Support load-balancing with Traeffik

Time left endpoint

A a logging / reporting / admin panel

Have a collecton of interesting containers to run:
- tor
- http proxy
    - in different countries (to stream video for example)
- zeronet client
- temporary bitcoin node (with a preloaded blockchain if it is doable in a costly manner)
