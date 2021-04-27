# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

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
ssh -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo rm docker-compose.yml
scp -i keypairs/keypair-instance1 docker-compose.yml ubuntu@$INSTANCE1:docker-compose.yml

# deploy in remote machine
ssh -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack rm $APP_NAME
ssh -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack deploy $APP_NAME -c docker-compose.yml