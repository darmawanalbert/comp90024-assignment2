import openstack
import os

SERVER_NAME = "python-instance"
conn = openstack.connect(cloud='comp90024')

flavor = conn.compute.find_flavor('uom.mse.2c9g')
network = conn.network.find_network('qh2-uom')
keypair = conn.compute.find_keypair('group1-keypair')

# create security group
example_sec_group = conn.network.create_security_group(name='comp90024-security-group')
example_rule = conn.network.create_security_group_rule(security_group_id=example_sec_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='80',port_range_min='80',ethertype='IPv4')
print(example_rule)
example_rule = conn.network.create_security_group_rule(security_group_id=example_sec_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='443',port_range_min='443',ethertype='IPv4')
print(example_rule)
example_rule = conn.network.create_security_group_rule(security_group_id=example_sec_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='22',port_range_min='22',ethertype='IPv4')
print(example_rule)
example_rule = conn.network.create_security_group_rule(security_group_id=example_sec_group.id,direction='ingress',remote_ip_prefix='0.0.0.0/0',protocol='tcp',port_range_max='8080',port_range_min='8080',ethertype='IPv4')
print(example_rule)

# create image
print(f'flavor: {flavor.id}')
print(f'network: {network.id}')
print(f'keypair: {keypair.name}')
server = conn.compute.create_server(name=SERVER_NAME, image_id='f8b79936-6616-4a22-b55d-0d0a1d27bceb', flavor_id=flavor.id,networks=[{"uuid": network.id}], key_name=keypair.name, security_groups=[{'name': 'comp90024-security-group'}])
server = conn.compute.wait_for_server(server)

print(server)