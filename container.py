# coding: utf-8

from docker import Client
import json, time
import netifaces as ni
import redis

DEFAULT_EXPIRATION = 360

db = redis.Redis('localhost')

def get_ip_address(ifname):
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
    expiration_ts     = ts + DEFAULT_EXPIRATION
    ip                = get_ip_address('eth0')
    inspection        = cli.inspect_container(container=container.get('Id'))
    host_binded_ports = {k:v[0]['HostPort'] for k,v in inspection['NetworkSettings']['Ports'].items()}

    db.set(container, expiration_ts)

    return {"public_ip":ip, "binded_ports":host_binded_ports, "container":container, "timestamp":ts}

def stop(id):
    pass

def remove(id):
    pass

def inspect(id):
    pass


# Run tests:
# params = {"image":"nginx:latest","ports":[80,443]}
# print(run(run_params=params))