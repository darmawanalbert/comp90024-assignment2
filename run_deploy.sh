sudo rm -r keypairs/*
sudo rm ~/.ssh/known_hosts; touch ~/.ssh/known_hosts
python3 deploy.py