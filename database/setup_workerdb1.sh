# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

# declare variables for the couchdb cluster setup
export workernode=45.113.234.166
export workerport=25984
export workerindex=1
export user='admin'
export pass='admin'
export VERSION='latest'
export cookie='a192aeb9904e6590849337933b000c99'

# pull from dockerhub ibmcom
sudo docker pull ibmcom/couchdb3:${VERSION}

# create docker container
# stops and removes the docker if already exist

if [ ! -z $(sudo docker ps --all --filter "name=workercouchdb${workerindex}" --quiet) ]
  then
    sudo docker stop workercouchdb${workerindex}
    sudo docker rm workercouchdb${workerindex}
fi

sudo docker create\
  --name workercouchdb${workerindex} -p\
  ${workerport}:5984\
  -v /opt/couchdb/worker${workerindex}/data:/opt/couchdb/data\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env COUCHDB_SECRET=${cookie}\\
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"workercouchdb${workerindex}\""\\
  couchdb:${VERSION}

# start the container
sudo docker start workercouchdb${workerindex}

sleep 10

sudo docker exec workercouchdb${workerindex} bash -c "echo \"-setcookie \"${cookie}\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec workercouchdb${workerindex} bash -c "echo \"-name \"workercouchdb${workerindex}\"\" >> /opt/couchdb/etc/vm.args"

sudo docker restart workercouchdb${workerindex}

sleep 5