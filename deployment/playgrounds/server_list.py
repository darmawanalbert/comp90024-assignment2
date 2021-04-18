import openstack
import subprocess as sp

SERVER_NAME = "python-instance"
conn = openstack.connect(cloud='comp90024')

for server in conn.compute.servers():
    print(server.addresses['qh2-uom'][0]['addr'])