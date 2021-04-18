import openstack
import os
import time
import subprocess as sp

SERVER_NAME_LIST = [{'name': 'instance1','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance1'},{'name': 'instance2','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance2'},{'name': 'instance3','flavor': 'uom.mse.2c9g','keypair': 'keypair-instance3'},{'name': 'instance4','flavor': 'uom.mse.2c9g','keypair': 'keypair-instance4'}]
SECURITY_GROUP_NAME = 'comp90024-security-group'
CLOUD_NAME = 'comp90024'
FLAVOR_NAME = 'uom.mse.2c9g'
NETWORK_NAME = 'qh2-uom'
KEYPAIR_NAME = 'group1-keypair'
PRIVATE_KEYPAIR_FILE = '../keypairs/group1-keypair.pem'
FOLDER_NAME = '../keypairs/'
IMAGE_NAME = 'NeCTAR Ubuntu 20.04 LTS (Focal) amd64'
conn = openstack.connect(cloud=CLOUD_NAME)

def get_image_id():
    print('image processed..')
    image_id = None
    for image in conn.image.images():
        if(image.name == IMAGE_NAME):
            image_id = image.id
            break
    return image_id

def get_keypair_name(keypair_name):
    print(f'keypair {keypair_name} processed..')
    keypair = conn.compute.find_keypair(keypair_name)
    if not keypair:
        keypair = conn.compute.create_keypair(name=keypair_name)
        with open(FOLDER_NAME + keypair_name, 'w') as f:
            f.write("%s" % keypair.private_key)
        os.chmod(FOLDER_NAME + keypair_name, 0o400)
    return keypair.name

def get_security_group_name():
    print('security group processed..')
    security_group = conn.network.find_security_group(SECURITY_GROUP_NAME)
    if not security_group:
        security_group = conn.network.create_security_group(name=SECURITY_GROUP_NAME)
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='80',port_range_min='80',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='443',port_range_min='443',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='22',port_range_min='22',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='8080',port_range_min='8080',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='2377',port_range_min='2377',ethertype='IPv4')
    return security_group.name

network = conn.network.find_network(NETWORK_NAME)
image_id = get_image_id()
security_group_name = get_security_group_name()
    
# create image
for server in SERVER_NAME_LIST:
    while True: # magic happens here.
        try:
            print("Sleeping for 5s ") # magic happens here.
            time.sleep(5)
            print(f"server {server['name']} processed..")
            flavor = conn.compute.find_flavor(server['flavor'])
            create_server = conn.compute.create_server(name=server['name'], image_id=image_id, flavor_id=flavor.id,networks=[{"uuid": network.id}], key_name=get_keypair_name(server['keypair']), security_groups=[{'name': security_group_name}])
            create_server = conn.compute.wait_for_server(create_server)
            print(f"server {server['name']} created.")
        except Exception as err:
            print(f"ERROR: {err}")
            continue
        break

for server in conn.compute.servers():
    while True: # magic happens here.
        try:
            print("Sleeping for 5s ") # magic happens here.
            time.sleep(5)
            print(f"name: {server.name} addr: {server.addresses[NETWORK_NAME][0]['addr']}, docker installing..")
            server_address = server.addresses[NETWORK_NAME][0]['addr'] + "," # magic happens here.
            command_bash = f"ansible-playbook instance.yml -u ubuntu -i {server_address} --private-key {FOLDER_NAME}keypair-{server.name}"
            result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
            output, error = result.communicate()
            if(error != None):
                print(f"{error}")
                print("retry..")
                continue
            if("UNREACHABLE!" in output.decode("utf-8")):
                print(output.decode("utf-8"))
                print("retry..")
                continue
            else:
                print(output.decode("utf-8"))
                print(f"name: {server.name} addr: {server.addresses[NETWORK_NAME][0]['addr']}, docker installed.")
        except Exception as err:
            print(f"ERROR: {err}")
            continue
        break
print('done.')