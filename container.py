# coding: utf-8
#!/usr/bin/env python3

from docker import Client
import json, time
import netifaces as ni
import redis
import os

# Configuration

try:
    DEFAULT_EXPIRATION = os.environ["DEFAULT_EXPIRATION"]
except KeyError:
    print("No DEFAULT_EXPIRATION environment variable set, defaulting to 360 seconds")
    DEFAULT_EXPIRATION = 360

# If a redis server is defined in environment then we use it, otherwise assumed local
try:
    REDIS = os.environ["REDIS"]
except KeyError:
    print("No REDIS environment variable set, defaulting to localhost:6379")
    REDIS = "localhost:6379"

# worker

db = redis.Redis(REDIS)

def get_ip_address(ifname):
    try:  
        return os.environ["IP"]
    except KeyError: 
        print("No IP environment variable set, defaulting to eth0")
        return ni.ifaddresses(ifname)[2][0]['addr']

cli = Client(base_url='unix://var/run/docker.sock')

def run(run_params):
    # first make sure the image has been pulled locally:
    try:
        res = cli.pull(run_params['image'])
        print(res)
    except(Exception) as error:
        raise error

    # Turn the port list into a dict
    binded_ports = {k:None for i, k in enumerate(run_params['ports'])}
    print(binded_ports)
    # Create container and bind to random host ports 
    try:
        container = cli.create_container(image=run_params['image'], ports=run_params['ports'], detach=True,
        host_config=cli.create_host_config(port_bindings=binded_ports))
    except(Exception) as error:
        raise error
    
    # And start it
    try:
        cli.start(container=container.get('Id'))
    except(Exception) as error:
        raise error

    container_id      = container['Id']
    ts                = time.time()
    expiration_ts     = ts + float(DEFAULT_EXPIRATION)
    ip                = get_ip_address('eth0')
    inspection        = cli.inspect_container(container=container.get('Id'))
    host_binded_ports = {k:v[0]['HostPort'] for k,v in inspection['NetworkSettings']['Ports'].items()}

    db.set(container_id, expiration_ts)

    res = {"public_ip":ip, "binded_ports":host_binded_ports, "container_id":container_id, \
    "timestamp":ts, "expiration_timestamp":expiration_ts}
    print("Just launched the following container:")
    print(res)
    return res

def ps():
    c = cli.containers()
    return c

def stop(id):
    cli.stop(id)
    print("Stopping container with id: %s" %id)

def remove(id):
    pass

def logs(id, lines=10):
    pass

def inspect(id):
    return cli.inspect_container(id)


# Run tests:
# params = {"image":"nginx:latest","ports":[80,443]}
# print(run(run_params=params))
