import openstack
import subprocess as sp

SERVER_NAME = "python-instance"
conn = openstack.connect(cloud='comp90024')

security_group = conn.network.find_security_group('comp90024-security-group')
print(security_group.name)