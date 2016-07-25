#!/usr/bin/env python3
# coding: utf-8

from docker import Client

cli = Client(base_url='unix://var/run/docker.sock')

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

