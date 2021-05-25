# COMP90024 Team 1
# Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
# Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
# I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
# Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au

# make sure keypair can be run
chmod 400 keypairs/keypair-instance1
chmod 400 keypairs/keypair-instance2
chmod 400 keypairs/keypair-instance3
chmod 400 keypairs/keypair-instance4

# build new images
docker-compose build
docker-compose push

# build new images
docker-compose -f harvesters/docker-compose.yml build
docker-compose -f harvesters/docker-compose.yml push

# set to execution file
chmod +x constants.sh
source constants.sh

# setup database couchdb
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance3 database/constants.sh ubuntu@$INSTANCE3:constants.sh
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance3 database/default.ini ubuntu@$INSTANCE3:default.ini
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance3 database/local.ini ubuntu@$INSTANCE3:local.ini
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance3 ubuntu@$INSTANCE3 sudo rm -r 
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance3 -r database/ ubuntu@$INSTANCE3:database/
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance3 ubuntu@$INSTANCE3 'bash -s' < ./database/setup_workerdb1.sh

scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 database/constants.sh ubuntu@$INSTANCE4:constants.sh
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 database/default.ini ubuntu@$INSTANCE4:default.ini
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 database/local.ini ubuntu@$INSTANCE4:local.ini
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo rm -r database/ 
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 -r database/ ubuntu@$INSTANCE4:database/
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 'bash -s' < ./database/setup_masterdb.sh
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 npm --prefix ./database/ install ./database/
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 grunt --gruntfile ./database/Gruntfile.js couch-compile
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 grunt --gruntfile ./database/Gruntfile.js couch-push

# setup harvester/docker-compose.yml
chmod 400 keypairs/keypair-instance4
# ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo rm -r harvesters/
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 harvesters/docker-compose.yml ubuntu@$INSTANCE4:harvesters.docker-compose.yml
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo docker pull wildananugrah/twitter_search
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo docker pull wildananugrah/twitter_collect
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo docker-compose -f harvesters.docker-compose.yml down
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance4 ubuntu@$INSTANCE4 sudo docker-compose -f harvesters.docker-compose.yml up -d

# copy docker-compose.yml
chmod 400 keypairs/keypair-instance1
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo rm docker-compose.yml
scp -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 docker-compose.yml ubuntu@$INSTANCE1:docker-compose.yml

# deploy service and frontend
# ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack rm $APP_NAME
ssh -o StrictHostKeyChecking=no -i keypairs/keypair-instance1 ubuntu@$INSTANCE1 sudo docker stack deploy $APP_NAME -c docker-compose.yml