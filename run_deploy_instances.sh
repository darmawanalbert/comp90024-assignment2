# pre-requisite
sudo rm -r keypairs/*
sudo rm ~/.ssh/known_hosts; touch ~/.ssh/known_hosts

# openrc setup
source openrc.sh

# deploy instances
python3 deploy.py