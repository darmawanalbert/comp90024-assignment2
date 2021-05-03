# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

import openstack
import os, shutil
import time
import subprocess as sp
from datetime import datetime
import glob
from pathlib import Path

SERVER_NAME_LIST = [
    {'name': 'instance1','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance1'},
    {'name': 'instance2','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance2'},
    {'name': 'instance3','flavor': 'uom.mse.1c4g','keypair': 'keypair-instance3'},
    {'name': 'instance4','flavor': 'uom.mse.2c9g','keypair': 'keypair-instance4'}
]

SECURITY_GROUP_NAME = 'comp90024-security-group'
NETWORK_NAME = 'qh2-uom'
FOLDER_NAME = 'keypairs/'
IMAGE_NAME = 'NeCTAR Ubuntu 20.04 LTS (Focal) amd64'
DEFAULT_USER = "ubuntu"
LOCAL_DOCKER_COMPOSE = "docker-compose.yml"
DOCKER_APP_NAME = "comp90024"
CREATE_INSTANCE_YML = "instance.yml"
DATABASE_SETUP_FOLDER = "database/"
HARVESTERS_FOLDER = "harvesters/"
LOCAL_NGINX_FOLDER = "nginx/"
LOCAL_NGINX_CONF = f"{LOCAL_NGINX_FOLDER}default.conf"
LOCAL_NGINX_DOCKER_COMPOSE = f"nginx.docker-compose.yml"
LOCAL_NGINX_DOCKER_FILE = f"nginx.Dockerfile"
LOCAL_CONSTANTS = f"constants.sh"

def create_connection(auth_url, project_name, username, password, region_name,
                      user_domain, project_domain, app_name, app_version):
    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region_name,
        user_domain_name=user_domain,
        project_domain_name=project_domain,
        app_name=app_name,
        app_version=app_version,
    )

def delete_all_instances(conn):
    for server in conn.compute.servers():
        while True: # magic happens here.
            try:
                print(f"Deleting {server.name} ") # magic happens here.
                time.sleep(5)
                conn.compute.delete_server(server)
            except Exception as err:
                print(f"ERROR: {err}")
                continue
            break

def delete_key_pairs(conn):
    for keypair in conn.compute.keypairs():
        while True: # magic happens here.
            try:
                print(f"Deleting {keypair.name} ") # magic happens here.
                time.sleep(5)
                conn.compute.delete_keypair(keypair)
            except Exception as err:
                print(f"ERROR: {err}")
                continue
            break

def get_image_id(conn):
    print('image processed..')
    image_id = None
    for image in conn.image.images():
        if(image.name == IMAGE_NAME):
            image_id = image.id
            break
    return image_id

def get_keypair_name(keypair_name, conn):
    print(f'keypair {keypair_name} processed..')
    keypair = conn.compute.find_keypair(keypair_name)
    if not keypair:
        keypair = conn.compute.create_keypair(name=keypair_name)
        with open(FOLDER_NAME + keypair_name, 'w') as f:
            f.write("%s" % keypair.private_key)
        os.chmod(FOLDER_NAME + keypair_name, 0o400)
    return keypair.name

def get_security_group_name(conn):
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

def create_instance(server_name_list, conn):
    for server in server_name_list:
        while True: # magic happens here.
            try:
                print("Sleeping for 5s ") # magic happens here.
                time.sleep(5)
                print(f"server {server['name']} processed..")
                flavor = conn.compute.find_flavor(server['flavor'])
                network = conn.network.find_network(NETWORK_NAME)
                image_id = get_image_id(conn)
                security_group_name = get_security_group_name(conn)
                create_server = conn.compute.create_server(name=server['name'], image_id=image_id, flavor_id=flavor.id,networks=[{"uuid": network.id}], key_name=get_keypair_name(server['keypair'], conn), security_groups=[{'name': security_group_name}])
                create_server = conn.compute.wait_for_server(create_server)
                print(f"server {server['name']} created.")
            except Exception as err:
                print(f"ERROR: {err}")
                server = conn.compute.find_server(server['name'])
                conn.compute.delete_server(server)
                continue
            break
        
def setup_docker(conn):
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
    server_list = {x: server_list[x] for x in server_list if x not in {'instance1','instance3','instance4'}}
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

def create_harvester_docker_compose(instance4):
    fin = open("templates/harvesters.docker-compose.yml.template", "rt")
    template = fin.read()
    template = template.replace('${INSTANCE4}', instance4)

    fin.close()

    fout = open("harvesters/docker-compose.yml", "wt")
    fout.write(template)
    fout.close()

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

def setup_nginx(instance1):
    print(f"Copy default.conf to remote machine [{instance1['addr']}].")
    command_bash = f"scp -oStrictHostKeyChecking=no -i {instance1['keypair']}  {LOCAL_NGINX_FOLDER}/default.conf {DEFAULT_USER}@{instance1['addr']}:default.conf "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"default.conf has been copied to remote machine [{instance1['addr']}].")

    print(f"Execute NGINX in instance1 [{instance1['addr']}].")
    command_bash = f"ssh -oStrictHostKeyChecking=no -i {instance1['keypair']} {DEFAULT_USER}@{instance1['addr']} sudo ufw allow 'Nginx HTTP' "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    command_bash = f"ssh -oStrictHostKeyChecking=no -i {instance1['keypair']} {DEFAULT_USER}@{instance1['addr']} sudo cp default.conf /etc/nginx/conf.d/load-balancer.conf "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    command_bash = f"ssh -oStrictHostKeyChecking=no -i {instance1['keypair']} {DEFAULT_USER}@{instance1['addr']} sudo rm /etc/nginx/sites-enabled/default "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    command_bash = f"ssh -oStrictHostKeyChecking=no -i {instance1['keypair']} {DEFAULT_USER}@{instance1['addr']} sudo systemctl restart nginx "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()

    print(f"NGINX has been setup in [{instance1['addr']}].")

def setup_docker_compose(instance1):
    # copy docker-compose
    print(f"Copy {LOCAL_DOCKER_COMPOSE} to remote machine [{instance1['addr']}].")
    command_bash = f"scp -oStrictHostKeyChecking=no -i {instance1['keypair']} {LOCAL_DOCKER_COMPOSE} {DEFAULT_USER}@{instance1['addr']}:{LOCAL_DOCKER_COMPOSE} "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"{LOCAL_DOCKER_COMPOSE} has been copied to remote machine [{instance1['addr']}].")

    # execute docker stack deploy -c docker-compose.yml
    print(f"Execute docker stack deploy {DOCKER_APP_NAME}.")
    command_bash = f"ssh -oStrictHostKeyChecking=no -i {instance1['keypair']} {DEFAULT_USER}@{instance1['addr']} sudo docker stack deploy {DOCKER_APP_NAME} -c {LOCAL_DOCKER_COMPOSE} "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    output = output.decode("utf-8").split('\n')
    print(output)

def setup_couchdb(instance4):
    print(f"Copy all {DATABASE_SETUP_FOLDER} folder to remote machine [{instance4['addr']}].")
    command_bash = f"scp -oStrictHostKeyChecking=no -i {instance4['keypair']} -r {DATABASE_SETUP_FOLDER} {DEFAULT_USER}@{instance4['addr']}:{DATABASE_SETUP_FOLDER} "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"{LOCAL_DOCKER_COMPOSE} has been copied to remote machine [{instance4['addr']}].")

    # set env variable
    print(f"Set up couchdb in instance4: {instance4['addr']}.")
    command_bash = f"ssh -oStrictHostKeyChecking=no -i {instance4['keypair']} {DEFAULT_USER}@{instance4['addr']} chmod +x {DATABASE_SETUP_FOLDER}setup_db.sh && sudo ./{DATABASE_SETUP_FOLDER}setup_db.sh "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    output = output.decode("utf-8").split('\n')
    print(output)

def setup_harvester(instance4):
    print(f"Copy all harvester folder to remote machine [{instance4['addr']}].")
    command_bash = f"scp -oStrictHostKeyChecking=no -i {instance4['keypair']} -r {HARVESTERS_FOLDER} {DEFAULT_USER}@{instance4['addr']}:{HARVESTERS_FOLDER} "
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"{HARVESTERS_FOLDER} has been copied to remote machine [{instance4['addr']}].")

    print(f"Execute harvester app [{instance4['addr']}].")
    command_bash = f"ssh -oStrictHostKeyChecking=no -i {instance4['keypair']} {DEFAULT_USER}@{instance4['addr']} sudo docker-compose -f {HARVESTERS_FOLDER}docker-compose.yml up -d"
    result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
    output, error = result.communicate()
    print(f"Execute harvester app in [{instance4['addr']}].")

def delete_local_keypairs():
    print("Deleting local keypairs.")
    folder = './keypairs/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    open(f'{os.path.expanduser("~")}/.ssh/known_hosts', 'w').close()
    print("Deleting local keypairs done.")

def deploy_all():
    try:
        conn = create_connection(os.getenv('OS_AUTH_URL'),os.getenv('OS_PROJECT_NAME'), os.getenv('OS_USERNAME'),os.getenv('OS_PASSWORD_INPUT'),os.getenv('OS_REGION_NAME'),os.getenv('OS_USER_DOMAIN_NAME'),os.getenv('OS_PROJECT_DOMAIN_ID'),os.getenv('OS_PROJECT_NAME'),os.getenv('OS_IDENTITY_API_VERSION'))

        # pre-requisite
        delete_local_keypairs()

        #delete instances, keypairs, and networks in nectar
        delete_all_instances(conn)
        delete_key_pairs(conn)

        # create instance
        create_instance(SERVER_NAME_LIST, conn)

        # docker, docker-compose, docker-machine
        server_list = setup_docker(conn)

        instance1 = server_list['instance1']
        instance4 = server_list['instance4']

        # get swarm join token
        swarm_join_token = swarm_init(instance1)

        # setup join swarm 
        setup_swarm_join(server_list, swarm_join_token)

        # setup couchdb
        setup_couchdb(instance4)

        # setup harvester
        create_harvester_docker_compose(instance4['addr'])
        setup_harvester(instance4)

        # create docker-compose.yml
        create_docker_compose(instance4['addr'])

        # setup docker compose
        setup_docker_compose(instance1)

        # create nginx/default.conf
        create_nginx_conf(server_list)
        create_constants_file(instance1['addr'])

        # setup nginx
        setup_nginx(instance1)
    except Exception as err:
        print(f"ERROR: {err}")

def update_app():
    try:
        conn = create_connection(os.getenv('OS_AUTH_URL'),os.getenv('OS_PROJECT_NAME'), os.getenv('OS_USERNAME'),os.getenv('OS_PASSWORD_INPUT'),os.getenv('OS_REGION_NAME'),os.getenv('OS_USER_DOMAIN_NAME'),os.getenv('OS_PROJECT_DOMAIN_ID'),os.getenv('OS_PROJECT_NAME'),os.getenv('OS_IDENTITY_API_VERSION'))
        instance1_addr = None
        for server in conn.compute.servers():
            if(server.name == 'instance1'):
                instance1_addr = server.addresses[NETWORK_NAME][0]['addr']
        
        print(f"Instance 1 ip address: {instance1_addr}")
        
        command_bash = f"docker-compose build "
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        output = output.decode("utf-8").split('\n')
        print(output)

        command_bash = f"docker-compose push "
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        output = output.decode("utf-8").split('\n')
        print(output)

        command_bash = f"ssh -i keypairs/keypair-instance1 ubuntu@{instance1_addr} sudo rm docker-compose.yml "
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        output = output.decode("utf-8").split('\n')
        print(output)

        command_bash = f"scp -i keypairs/keypair-instance1 docker-compose.yml ubuntu@{instance1_addr}:docker-compose.yml "
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        output = output.decode("utf-8").split('\n')
        print(output)

        command_bash = f"ssh -i keypairs/keypair-instance1 ubuntu@{instance1_addr} sudo docker stack rm comp90024 "
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        output = output.decode("utf-8").split('\n')
        print(output)

        print("Sleep 10s")
        time.sleep(10)

        command_bash = f"ssh -i keypairs/keypair-instance1 ubuntu@{instance1_addr} sudo docker stack deploy comp90024 -c docker-compose.yml "
        result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
        output, error = result.communicate()
        output = output.decode("utf-8").split('\n')
        print(output)

    except Exception as err:
        print(f"ERROR: {err}")

def clear_screen():
    for i in range(50):
        print("\n")

def screen_menu():
    print("== Indo Nerdz Deployer! ==")
    print("1. Deploy ALL")
    print("2. Update App")
    print("Press q to quit.")

def main():
    try:

        while True:
            clear_screen()
            screen_menu()
            _input = input('choose: ')
            if _input == "1":
                start = datetime.now()
                print(f"started at {start}")

                deploy_all()

                print('done.')
                end = datetime.now()
                print(f"ended at {end}, in {end - start}")

                input('press ENTER to continue')
                # deploy_all()
            elif _input == "2":
                start = datetime.now()
                print(f"started at {start}")

                update_app()
                
                end = datetime.now()
                print(f"ended at {end}, in {end - start}")
                input('press ENTER to continue')
            elif _input == "q":
                exit()
            else:
                print("please type correct input!")
                input('press ENTER to continue')
                continue

    except Exception as err:
        print(f"ERROR: {err}")

if __name__ == "__main__":
    main()