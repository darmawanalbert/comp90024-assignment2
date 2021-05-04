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
docker-compose push

# build new images
docker-compose -f harvesters/docker-compose.yml build
docker-compose -f harvesters/docker-compose.yml push

# set to execution file
chmod +x constants.sh
source constants.sh

# copy docker-compose.yml
chmod 400 keypairs/keypair-instance1
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo rm docker-compose.yml
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 docker-compose.yml ubuntu@$INSTANCE1:docker-compose.yml

# deploy in remote machine
# ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack rm $APP_NAME
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack deploy $APP_NAME -c docker-compose.yml

# copy harvester/docker-compose.yml
chmod 400 keypairs/keypair-instance4
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo rm -r harvesters/
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 -r harvesters/ ubuntu@$INSTANCE4:harvesters/
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo docker-compose -f harvesters/docker-compose.yml pull
# ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo docker-compose -f harvesters/docker-compose.yml push
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo docker-compose -f harvesters/docker-compose.yml up --force-recreate --build -d
