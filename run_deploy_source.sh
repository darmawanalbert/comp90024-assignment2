# remove all container in local machine
# docker container stop $(docker container ls -aq)
# docker container rm $(docker container ls -aq)

# remove all image in local machine
# docker image rm $(docker images -aq)

# build new images
docker-compose build

# push new image to docker hub
docker-compose push

# set to execution file
chmod +x constants.sh
source constants.sh

# copy docker-compose.yml
chmod 400 keypairs/keypair-instance1
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo rm docker-compose.yml
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 docker-compose.yml ubuntu@$INSTANCE1:docker-compose.yml

# deploy in remote machine
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack rm $APP_NAME
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack deploy $APP_NAME -c docker-compose.yml