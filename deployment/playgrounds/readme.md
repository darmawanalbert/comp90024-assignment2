- OpenStack password: NWNmM2I1YjRkZTlhMzUz
- xyz=""; if [ -z "$xyz" ] ; then echo "true"; else echo "false"; fi
- scp -i keypairs/group1-keypair.pem -r ./playgrounds/ ubuntu@45.113.232.250:playgrounds/
- scp -i keypairs/group1-keypair.pem -r ./keypairs/ ubuntu@115.146.95.50:keypairs/
- ssh -i keypairs/group1-keypair.pem ubuntu@45.113.232.250
- ssh -i keypairs/group1-keypair.pem ubuntu@172.26.132.163
- openstack server create --flavor 5d8b8337-dc22-4ac7-9d4c-fda749d364bf --image f8b79936-6616-4a22-b55d-0d0a1d27bceb --key-name group1-keypair --security-group ssh --network qh2-uom frontend
- openstack security group list
- openstack security group rule list default
- openstack keypair list
- openstack image list
- openstack flavor list
- https://www.youtube.com/watch?v=U6SlST9tQ6k replication DB
- https://www.youtube.com/watch?v=c60DGao6sls views and mapreduce couchDB
- https://takacsmark.com/docker-swarm-tutorial-for-beginners/ docker 
- https://docker-py.readthedocs.io/en/stable/index.html
- https://github.com/openstack/openstacksdk
- https://docs.openstack.org/mitaka/user-guide/sdk.html
- name: instance4 addr: 45.113.233.153
- name: instance3 addr: 45.113.235.236
- name: instance2 addr: 45.113.232.233
- name: instance1 addr: 45.113.232.231
- ansible-playbook instance1.yml -u ubuntu -i 45.113.233.153,45.113.235.236,45.113.232.233,45.113.232.231 --private-key ../keypairs/group1-keypair.pem
- sudo apt install ansible


## result log
```
image processed..
security group processed..
Sleeping for 5s 
server instance1 processed..
keypair keypair-instance1 processed..
server instance1 created.
Sleeping for 5s 
server instance2 processed..
keypair keypair-instance2 processed..
server instance2 created.
Sleeping for 5s 
server instance3 processed..
keypair keypair-instance3 processed..
server instance3 created.
Sleeping for 5s 
server instance4 processed..
keypair keypair-instance4 processed..
server instance4 created.
Sleeping for 5s 
name: instance4 addr: 45.113.235.63, docker installing..

PLAY [all] *****************************************************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************************
fatal: [45.113.235.63]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: connect to host 45.113.235.63 port 22: Connection timed out", "unreachable": true}

PLAY RECAP *****************************************************************************************************************************************************************
45.113.235.63              : ok=0    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0   


retry..
Sleeping for 5s 
name: instance4 addr: 45.113.235.63, docker installing..

PLAY [all] *****************************************************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************************
fatal: [45.113.235.63]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: connect to host 45.113.235.63 port 22: Connection refused", "unreachable": true}

PLAY RECAP *****************************************************************************************************************************************************************
45.113.235.63              : ok=0    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0   


retry..
Sleeping for 5s 
name: instance4 addr: 45.113.235.63, docker installing..
The authenticity of host '45.113.235.63 (45.113.235.63)' can't be established.
ECDSA key fingerprint is SHA256:afZkGPgsrLulKaS/ZIB75WoIrYkBF84RC6ACu9k6VZo.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

PLAY [all] *****************************************************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************************
ok: [45.113.235.63]

TASK [Install aptitude using apt] ******************************************************************************************************************************************
changed: [45.113.235.63]

TASK [Install required system packages] ************************************************************************************************************************************
changed: [45.113.235.63] => (item=apt-transport-https)
ok: [45.113.235.63] => (item=ca-certificates)
changed: [45.113.235.63] => (item=curl)
ok: [45.113.235.63] => (item=software-properties-common)
changed: [45.113.235.63] => (item=python3-pip)
changed: [45.113.235.63] => (item=virtualenv)
ok: [45.113.235.63] => (item=python3-setuptools)

TASK [Add Docker GPG apt Key] **********************************************************************************************************************************************
changed: [45.113.235.63]

TASK [Add Docker Repository] ***********************************************************************************************************************************************
changed: [45.113.235.63]

TASK [Update apt and install docker-ce] ************************************************************************************************************************************
changed: [45.113.235.63]

TASK [Update apt and install docker-compose] *******************************************************************************************************************************
changed: [45.113.235.63]

PLAY RECAP *****************************************************************************************************************************************************************
45.113.235.63              : ok=7    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


name: instance4 addr: 45.113.235.63, docker installed.
Sleeping for 5s 
name: instance3 addr: 45.113.232.136, docker installing..
The authenticity of host '45.113.232.136 (45.113.232.136)' can't be established.
ECDSA key fingerprint is SHA256:VWvNQ55uqJnklK7HA4sivfKbBR8oxYrnLlbdkMSE9jY.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

PLAY [all] *****************************************************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************************
ok: [45.113.232.136]

TASK [Install aptitude using apt] ******************************************************************************************************************************************
changed: [45.113.232.136]

TASK [Install required system packages] ************************************************************************************************************************************
changed: [45.113.232.136] => (item=apt-transport-https)
ok: [45.113.232.136] => (item=ca-certificates)
changed: [45.113.232.136] => (item=curl)
ok: [45.113.232.136] => (item=software-properties-common)
changed: [45.113.232.136] => (item=python3-pip)
changed: [45.113.232.136] => (item=virtualenv)
ok: [45.113.232.136] => (item=python3-setuptools)

TASK [Add Docker GPG apt Key] **********************************************************************************************************************************************
changed: [45.113.232.136]

TASK [Add Docker Repository] ***********************************************************************************************************************************************
changed: [45.113.232.136]

TASK [Update apt and install docker-ce] ************************************************************************************************************************************
changed: [45.113.232.136]

TASK [Update apt and install docker-compose] *******************************************************************************************************************************
changed: [45.113.232.136]

PLAY RECAP *****************************************************************************************************************************************************************
45.113.232.136             : ok=7    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


name: instance3 addr: 45.113.232.136, docker installed.
Sleeping for 5s 
name: instance2 addr: 45.113.235.236, docker installing..
The authenticity of host '45.113.235.236 (45.113.235.236)' can't be established.
ECDSA key fingerprint is SHA256:zpm7osOHQEunrLhNpPanmiiDdk/aEO+L+a21oiEVR0I.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

PLAY [all] *****************************************************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************************
ok: [45.113.235.236]

TASK [Install aptitude using apt] ******************************************************************************************************************************************
changed: [45.113.235.236]

TASK [Install required system packages] ************************************************************************************************************************************
changed: [45.113.235.236] => (item=apt-transport-https)
ok: [45.113.235.236] => (item=ca-certificates)
changed: [45.113.235.236] => (item=curl)
ok: [45.113.235.236] => (item=software-properties-common)
changed: [45.113.235.236] => (item=python3-pip)
changed: [45.113.235.236] => (item=virtualenv)
ok: [45.113.235.236] => (item=python3-setuptools)

TASK [Add Docker GPG apt Key] **********************************************************************************************************************************************
changed: [45.113.235.236]

TASK [Add Docker Repository] ***********************************************************************************************************************************************
changed: [45.113.235.236]

TASK [Update apt and install docker-ce] ************************************************************************************************************************************
changed: [45.113.235.236]

TASK [Update apt and install docker-compose] *******************************************************************************************************************************
changed: [45.113.235.236]

PLAY RECAP *****************************************************************************************************************************************************************
45.113.235.236             : ok=7    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


name: instance2 addr: 45.113.235.236, docker installed.
Sleeping for 5s 
name: instance1 addr: 45.113.232.164, docker installing..
The authenticity of host '45.113.232.164 (45.113.232.164)' can't be established.
ECDSA key fingerprint is SHA256:Xp/NDPOOGimEqQ+sOE5Xs8bvovk+kYtk3W4/gL7Q8sE.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes 

PLAY [all] *****************************************************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************************
ok: [45.113.232.164]

TASK [Install aptitude using apt] ******************************************************************************************************************************************
changed: [45.113.232.164]

TASK [Install required system packages] ************************************************************************************************************************************
changed: [45.113.232.164] => (item=apt-transport-https)
ok: [45.113.232.164] => (item=ca-certificates)
changed: [45.113.232.164] => (item=curl)
ok: [45.113.232.164] => (item=software-properties-common)
changed: [45.113.232.164] => (item=python3-pip)
changed: [45.113.232.164] => (item=virtualenv)
ok: [45.113.232.164] => (item=python3-setuptools)

TASK [Add Docker GPG apt Key] **********************************************************************************************************************************************
changed: [45.113.232.164]

TASK [Add Docker Repository] ***********************************************************************************************************************************************
changed: [45.113.232.164]

TASK [Update apt and install docker-ce] ************************************************************************************************************************************
changed: [45.113.232.164]

TASK [Update apt and install docker-compose] *******************************************************************************************************************************
changed: [45.113.232.164]

PLAY RECAP *****************************************************************************************************************************************************************
45.113.232.164             : ok=7    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


name: instance1 addr: 45.113.232.164, docker installed.
done.
```