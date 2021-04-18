#!/bin/bash

source openrc.sh
# create security group
echo "create security group"
sleep 5
openstack security group create g1_security_group --description "Group 1 Security Group"
sleep 5
openstack security group rule create g1_security_group --protocol tcp --dst-port 80:80 --remote-ip 0.0.0.0/0
sleep 5
openstack security group rule create g1_security_group --protocol tcp --dst-port 443:443 --remote-ip 0.0.0.0/0
sleep 5
openstack security group rule create g1_security_group --protocol tcp --dst-port 22:22 --remote-ip 0.0.0.0/0
sleep 5
openstack security group rule create g1_security_group --protocol tcp --dst-port 8080:8080 --remote-ip 0.0.0.0/0

# create instances
echo "create instance 1"
sleep 5
openstack server create --flavor 5d8b8337-dc22-4ac7-9d4c-fda749d364bf --image f8b79936-6616-4a22-b55d-0d0a1d27bceb --key-name group1-keypair --security-group g1_security_group --network qh2-uom instance_1

echo "create instance 2"
sleep 5
openstack server create --flavor 5d8b8337-dc22-4ac7-9d4c-fda749d364bf --image f8b79936-6616-4a22-b55d-0d0a1d27bceb --key-name group1-keypair --security-group g1_security_group --network qh2-uom instance_2

echo "create instance 3"
sleep 5
openstack server create --flavor 5d8b8337-dc22-4ac7-9d4c-fda749d364bf --image f8b79936-6616-4a22-b55d-0d0a1d27bceb --key-name group1-keypair --security-group g1_security_group --network qh2-uom instance_3

echo "create instance 4"
sleep 5
openstack server create --flavor 5d8b8337-dc22-4ac7-9d4c-fda749d364bf --image f8b79936-6616-4a22-b55d-0d0a1d27bceb --key-name group1-keypair --security-group g1_security_group --network qh2-uom instance_4