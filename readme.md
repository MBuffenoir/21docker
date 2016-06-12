# 21 Docker

# Requirements

Have docker toolbox installed and cs configured to run command on exoscale API.

# Create a docker machine to run the container on:

    docker-machine create --driver exoscale \
        --exoscale-api-key $CLOUDSTACK_KEY \
        --exoscale-api-secret-key $CLOUDSTACK_SECRET_KEY \
        --exoscale-instance-profile small \
        --exoscale-disk-size 10 \
        --exoscale-security-group 21docker \
        21host


Start a redis server on our host with:

    docker run --name redis -p 127.0.0.1:6379:6379 -d redis redis-server --appendonly yes

Ssh to the host:

    docker-machine ssh 21host

Run the following commands:

    sudo apt-get update
    sudo apt-get -y install python-dev
    sudo easy_install3 -U pip
    pip install -r requirements.txt

# Client config

input json

{
    "image":"url or hub name",
    "ports":"1234",
    {
        "environment":[
            "name":"value",
            "name":"value"
            ]
    },
    "command":"/bin/sleep -t 30"
}

Will exposed default EXPOSE porst if needed on a random free port

container_name defaulting to docker's daily feeling

output json:

{
    "timestamp":timestamp,
    "id":"docker_container_id",
}

# CURL

curl -i \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{"image":"nginx:latest","ports":[80,443]}' \
    http://$(docker-machine ip blog):5000/docker/run/

To define udp port use: ``"ports":[(53, 'udp'), 5000]}
