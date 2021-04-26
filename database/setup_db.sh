# adding user to docker so can use docker without sudo
# sudo usermod -aG docker ${ubuntu}
# su - ${ubuntu}

# sleep 5

# declare variables for the couchdb cluster setup
export declare -a nodes=(115.146.95.84 45.113.235.136 45.113.233.153)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export 
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export user='admin'
export pass='admin'
export VERSION='latest'
export cookie='a192aeb9904e6590849337933b000c99'

# pull from dockerhub ibmcom
sudo docker pull ibmcom/couchdb3:${VERSION}

# create docker container
# stops and removes the docker if already exist

for node in "${nodes[@]}" 
  do
    if [ ! -z $(sudo docker ps --all --filter "name=couchdb${node}" --quiet) ] 
       then
         sudo docker stop $(sudo docker ps --all --filter "name=couchdb${node}" --quiet) 
         sudo docker rm $(sudo docker ps --all --filter "name=couchdb${node}" --quiet)
    fi 
done

for node in "${nodes[@]}" 
  do
    sudo docker create\
      --name couchdb${node}\
      -p 5984:5984\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${node}\""\
      ibmcom/couchdb3:${VERSION}
done

# put in const in docker container IDs
declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

# start the containers
for cont in "${conts[@]}"; do sudo docker start ${cont}; done

# sleep for 10s after starting
sleep 10

# setup the couchdb cluster
for node in ${othernodes} 
do
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\",\
             \"remote_node\": \"${node}\", \"node_count\": \"$(echo ${nodes[@]} | wc -w)\",\
             \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done

for node in ${othernodes}
do
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"${node}\",\
             \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
done

# # create worker master
# docker run --name db-worker -p 25984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin -e NODENAME=db-worker -v /couchworkerdata:/opt/couchdb/data  -d couchdb:latest

# # setup couchdb network
# docker network create couchdbnet
# docker network connect couchdbnet db-master
# docker network connect couchdbnet db-worker

# # sleep 5s
# sleep 5

# # create database
# curl -X PUT http://admin:admin@127.0.0.1:15984/testdb

# # setup cluster
# curl -X PUT http://admin:admin@127.0.0.1:15984/_users

# curl -X PUT http://admin:admin@127.0.0.1:15984/_replicator

# curl -X PUT http://admin:admin@127.0.0.1:15984/_global_changes

# curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "node_count":"3"}'

# curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "port": 5984, "node_count": "3", "remote_node": "db-worker", "remote_current_user": "admin", "remote_current_password": "admin" }'
# curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "add_node", "host":"db-worker", "port": "5984", "username": "admin", "password":"admin"}'

# curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "finish_cluster"}'

# # setup replicator
# curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_replicator -d '{"_id": "my_rep","source": "http://admin:admin@localhost:5984/testdb","target":  "http://admin:admin@db-worker:5984/testdb","create_target":  true,"continuous": true}'

# # temp
# curl -X GET http://admin:admin@127.0.0.1:15984/_all_dbs

# curl -X GET http://admin:admin@127.0.0.1:15984/_scheduler/docs/_replicator/my_rep
