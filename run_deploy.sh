# remove all container in local machine
docker container stop $(docker container ls -aq)
docker container rm $(docker container ls -aq)

# remove all image in local machine
docker image rm $(docker images -aq)

# build new images
docker-compose build

# push new image to docker hub
docker-compose push 

# pre-requisite
sudo rm -r keypairs/*
sudo rm ~/.ssh/known_hosts; touch ~/.ssh/known_hosts

# deploy instances
python3 deploy.py