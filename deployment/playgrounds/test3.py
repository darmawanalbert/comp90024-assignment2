import openstack
import subprocess as sp
CLOUD_NAME = 'comp90024'
conn = openstack.connect(cloud=CLOUD_NAME)

for server in conn.compute.servers():
    print("Sleeping for 5s ") # magic happens here.
    time.sleep(5)
    print(f"name: {server.name} addr: {server.addresses[NETWORK_NAME][0]['addr']}, docker installing..")
    server_address = server.addresses[NETWORK_NAME][0]['addr'] + "," # magic happens here.
    command_bash = f"ansible-playbook instance.yml -u ubuntu -i {server_address} --private-key {FOLDER_NAME}keypair-{server.name}"
    sp.call(command_bash.split())
    print(f"name: {server.name} addr: {server.addresses[NETWORK_NAME][0]['addr']}, docker installed.")