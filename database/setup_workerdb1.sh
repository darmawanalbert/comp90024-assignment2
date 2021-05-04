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
sudo docker network create --driver bridge couch

# create docker container
# stops and removes the docker if already exist

if [ ! -z $(sudo docker ps --all --filter "name=workercouchdb${workerindex}" --quiet) ]
  then
    sudo docker stop workercouchdb${workerindex}
    sudo docker rm workercouchdb${workerindex}
fi

sudo docker create\
  --name workercouchdb${workerindex}\
  --net=couch\
  --hostname couchdb@${workernode}\
  -p ${workerport}:5984\
  -p 4369:4369\
  -p 9100:9100\
  -v /opt/couchdb/worker${workerindex}/data:/opt/couchdb/data\
  --env NODENAME=couchdb@${workernode}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env COUCHDB_SECRET=${cookie}\
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${workernode}\"\
  -kernel \"inet_dist_listen_min 9100\" -kernel \"inet_dist_listen_max 9100\""\
  couchdb:${VERSION}

# start the container
sudo docker start workercouchdb${workerindex}

sleep 10

sudo docker exec workercouchdb${workerindex} bash -c "echo \"-setcookie \"${cookie}\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec workercouchdb${workerindex} bash -c "echo \"-name \"couchdb@${workernode}\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec workercouchdb${workerindex} bash -c "echo \"-kernel \"inet_dist_listen_min\" \"9100\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec workercouchdb${workerindex} bash -c "echo \"-kernel \"inet_dist_listen_max\" \"9100\"\" >> /opt/couchdb/etc/vm.args"

sudo docker restart workercouchdb${workerindex}

sleep 5