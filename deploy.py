# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

import openstack
import os
import time
import subprocess as sp
from datetime import datetime

SERVER_NAME_LIST = [
    {'name': 'instance1','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance1'},
    {'name': 'instance2','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance2'},
    {'name': 'instance3','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance3'},
    {'name': 'instance4','flavor': 'uom.mse.2c9g','keypair': 'keypair-instance4'}
]

SECURITY_GROUP_NAME = 'comp90024-security-group'
CLOUD_NAME = 'comp90024'
NETWORK_NAME = 'qh2-uom'
FOLDER_NAME = 'keypairs/'
IMAGE_NAME = 'NeCTAR Ubuntu 20.04 LTS (Focal) amd64'
DEFAULT_USER = "ubuntu"
LOCAL_DOCKER_COMPOSE = "docker-compose.yml"
DOCKER_APP_NAME = "comp90024"
CREATE_INSTANCE_YML = "instance.yml"
DATABASE_SETUP_FOLDER = "database/"
LOCAL_NGINX_FOLDER = "nginx/"
LOCAL_NGINX_CONF = f"{LOCAL_NGINX_FOLDER}default.conf"
LOCAL_NGINX_DOCKER_COMPOSE = f"nginx.docker-compose.yml"
LOCAL_NGINX_DOCKER_FILE = f"nginx.Dockerfile"
LOCAL_CONSTANTS = f"constans.sh"

conn = openstack.connect(cloud=CLOUD_NAME)

def delete_all_instances():
    for server in conn.compute.servers():
        while True: # magic happens here.
            try:
                print("Sleeping for 5s ") # magic happens here.
                time.sleep(5)
                conn.compute.delete_server(server)
            except Exception as err:
                print(f"ERROR: {err}")
                continue
            break

def delete_key_pairs():
    for keypair in conn.compute.keypairs()
    while True: # magic happens here.
        try:
            print("Sleeping for 5s ") # magic happens here.
            time.sleep(5)
            conn.compute.delete_keypair(keypair)
        except Exception as err:
            print(f"ERROR: {err}")
            continue
        break

def delete_network(network_name):
    print("Delete Network:")

    networks = conn.network.find_network()

    for subnet in networks.subnet_ids:
        conn.network.delete_subnet(subnet, ignore_missing=False)

    conn.network.delete_network(networks, ignore_missing=False)

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
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='81',port_range_min='81',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='443',port_range_min='443',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='22',port_range_min='22',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='8080',port_range_min='8080',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='2377',port_range_min='2377',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='15984',port_range_min='15984',ethertype='IPv4')
        conn.network.create_security_group_rule(security_group_id=security_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='25984',port_range_min='25984',ethertype='IPv4')
    return security_group.name

def create_instance(server_name_list):
    for server in server_name_list:
        while True: # magic happens here.
            try:
                print("Sleeping for 5s ") # magic happens here.
                time.sleep(5)
                print(f"server {server['name']} processed..")
                flavor = conn.compute.find_flavor(server['flavor'])
                network = conn.network.find_network(NETWORK_NAME)
                image_id = get_image_id()
                security_group_name = get_security_group_name()
                create_server = conn.compute.create_server(name=server['name'], image_id=image_id, flavor_id=flavor.id,networks=[{"uuid": network.id}], key_name=get_keypair_name(server['keypair']), security_groups=[{'name': security_group_name}])
                create_server = conn.compute.wait_for_server(create_server)
                print(f"server {server['name']} created.")
            except Exception as err:
                print(f"ERROR: {err}")
                server = conn.compute.find_server(server['name'])
                conn.compute.delete_server(server)
                continue
            break
        
def setup_docker():
    server_list = {}
    for server in conn.compute.servers():
        while True: # magic happens here.
            try:
                print("Sleeping for 5s ") # magic happens here.
                time.sleep(5)
                print(f"name: {server.name} addr: {server.addresses[NETWORK_NAME][0]['addr']}, docker installing..")
                server_address = server.addresses[NETWORK_NAME][0]['addr'] + "," # magic happens here.
                command_bash = f"ansible-playbook {CREATE_INSTANCE_YML} -u ubuntu -i {server_address} --private-key {FOLDER_NAME}keypair-{server.name}"
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
                if("FAILED!" in output.decode("utf-8")): 
                    print(output.decode("utf-8"))
                    print("retry..")
                    continue
                else:
                    print(output.decode("utf-8"))
                    print(f"name: {server.name} addr: {server.addresses[NETWORK_NAME][0]['addr']}, docker installed.")
            except Exception as err:
                print(f"ERROR: {err}")
                continue
            server_list[server.name] = { 'addr' : server.addresses[NETWORK_NAME][0]['addr'], 'keypair' : f'{FOLDER_NAME}keypair-{server.name}' }
            break
    return server_list

def swarm_leave(server_instance1):
    try:
        command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_instance1['keypair']} {DEFAULT_USER}@{server_instance1['addr']} sudo docker swarm leave -f"
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        output = output.decode("utf-8").split('\n')
        print(output)
        return True
    except Exception as err:
        print(f"ERROR {err}")
        return False

def swarm_init(server_instance1):
    try:
        command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_instance1['keypair']} {DEFAULT_USER}@{server_instance1['addr']} sudo docker swarm init"
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        all_output = output.decode("utf-8").split('\n')
        get_token = None
        for line in all_output:
            if("--token" in line.strip()):
                get_token = line.strip()
        print(get_token)
        return get_token
    except Exception as err:
        print(f"ERROR: {err}")
        return False

def setup_swarm_join(server_list, token_join_swarm):
    server_list = {x: server_list[x] for x in server_list if x not in {'instance1','instance4'}}
    for server in server_list:
        print(server)
        try:
            command_bash = f"ssh -i {server_list[server]['keypair']} {DEFAULT_USER}@{server_list[server]['addr']} sudo {token_join_swarm}"
            result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
            output, error = result.communicate()
            output = output.decode("utf-8")
            print(output)
        except Exception as err:
            print(f"ERROR {err}")

def create_docker_compose(instance4):
    
    fin = open("templates/docker-compose.template", "rt")
    
    fout = open(LOCAL_DOCKER_COMPOSE, "wt")
    
    for line in fin:
        
        fout.write(line.replace('${INSTANCE4}', instance4))
        
    fin.close()
    fout.close()

def create_nginx_conf(server_list):

    fin = open("templates/default.conf.template", "rt")
    template = fin.read()
    template = template.replace('${INSTANCE1}', server_list['instance1']['addr'])
    template = template.replace('${INSTANCE2}', server_list['instance2']['addr'])
    template = template.replace('${INSTANCE3}', server_list['instance3']['addr'])

    fin.close()

    fout = open(LOCAL_NGINX_CONF, "wt")
    fout.write(template)
    fout.close()

def create_constants_file(instance1):

    fin = open("templates/constants.template", "rt")
    template = fin.read()
    template = template.replace('${INSTANCE1}', instance1)

    fin.close()

    fout = open(LOCAL_CONSTANTS, "wt")
    fout.write(template)
    fout.close()

start = datetime.now()
print(f"started at {start}")

#delete instances, keypairs, and networks in nectar
delete_all_instances()
delete_key_pairs()
delete_network(NETWORK_NAME)

# create instance
create_instance(SERVER_NAME_LIST)

# docker, docker-compose, docker-machine
server_list = setup_docker()

# get swarm join token
swarm_join_token = swarm_init(server_list['instance1'])

# setup join swarm 
setup_swarm_join(server_list, swarm_join_token)
                
try:

    print(f"Copy all {DATABASE_SETUP_FOLDER} folder to remote machine [{server_list['instance4']['addr']}].")
    command_bash = f"scp -oStrictHostKeyChecking=no -i {server_list['instance4']['keypair']} -r {DATABASE_SETUP_FOLDER} {DEFAULT_USER}@{server_list['instance4']['addr']}:{DATABASE_SETUP_FOLDER} "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"{LOCAL_DOCKER_COMPOSE} has been copied to remote machine [{server_list['instance1']['addr']}].")

    # set env variable
    print(f"Set up couchdb in instance4: {server_list['instance4']['addr']}.")
    command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_list['instance4']['keypair']} {DEFAULT_USER}@{server_list['instance4']['addr']} chmod +x {DATABASE_SETUP_FOLDER}setup_db.sh && sudo ./{DATABASE_SETUP_FOLDER}setup_db.sh "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    output = output.decode("utf-8").split('\n')
    print(output)

    # create docker-compose.yml
    create_docker_compose(server_list['instance4']['addr'])

    # create docker-compose.yml
    create_ipdeploy(server_list['instance1']['addr'])

    # copy docker-compose
    print(f"Copy {LOCAL_DOCKER_COMPOSE} to remote machine [{server_list['instance1']['addr']}].")
    command_bash = f"scp -oStrictHostKeyChecking=no -i {server_list['instance1']['keypair']} {LOCAL_DOCKER_COMPOSE} {DEFAULT_USER}@{server_list['instance1']['addr']}:{LOCAL_DOCKER_COMPOSE} "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"{LOCAL_DOCKER_COMPOSE} has been copied to remote machine [{server_list['instance1']['addr']}].")

    # execute docker stack deploy -c docker-compose.yml
    print(f"Execute docker stack deploy {DOCKER_APP_NAME}.")
    command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_list['instance1']['keypair']} {DEFAULT_USER}@{server_list['instance1']['addr']} sudo docker stack deploy {DOCKER_APP_NAME} -c {LOCAL_DOCKER_COMPOSE} "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    output = output.decode("utf-8").split('\n')
    print(output)

    # create nginx/default.conf
    create_nginx_conf(server_list)
    create_constants_file(server_list['instance1']['addr'])

    # copy nginx/
    print(f"Copy default.conf to remote machine [{server_list['instance1']['addr']}].")
    command_bash = f"scp -oStrictHostKeyChecking=no -i {server_list['instance1']['keypair']}  {LOCAL_NGINX_FOLDER}/default.conf {DEFAULT_USER}@{server_list['instance1']['addr']}:default.conf "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"default.conf has been copied to remote machine [{server_list['instance1']['addr']}].")

    # execute nginx
    print(f"Execute NGINX in instance1 [{server_list['instance1']['addr']}].")
    command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_list['instance1']['keypair']} {DEFAULT_USER}@{server_list['instance1']['addr']} sudo ufw allow 'Nginx HTTP' "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_list['instance1']['keypair']} {DEFAULT_USER}@{server_list['instance1']['addr']} sudo cp default.conf /etc/nginx/conf.d/load-balancer.conf "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_list['instance1']['keypair']} {DEFAULT_USER}@{server_list['instance1']['addr']} sudo rm /etc/nginx/sites-enabled/default "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    command_bash = f"ssh -oStrictHostKeyChecking=no -i {server_list['instance1']['keypair']} {DEFAULT_USER}@{server_list['instance1']['addr']} sudo systemctl restart nginx "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    print(f"NGINX has been setup in [{server_list['instance1']['addr']}].")


except Exception as err:
    print(f"ERROR: {err}")

print('done.')
end = datetime.now()
print(f"ended at {end}, in {end - start}")