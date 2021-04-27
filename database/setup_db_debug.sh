# declare variables for the couchdb cluster setup
export declare -a nodes=(115.146.95.84 45.113.235.136 45.113.233.153)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export declare -a ports=(15984 25984 35984)
export masterport=`echo ${ports} | cut -f1 -d' '`
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export declare -a otherports=`echo ${ports[@]} | sed s/${masterport}//`
export declare -a indexdb=(1 2 3)
export size=${#nodes[@]}
export sizeworker=${#othernodes[@]}
export mastervolume='/opt/couchdb/master/data:/opt/couchdb/data'
export user='admin'
export pass='admin'
export VERSION='latest'
export cookie='a192aeb9904e6590849337933b000c99'

# pull from dockerhub ibmcom
# sudo docker pull ibmcom/couchdb3:${VERSION}
sudo docker pull couchdb:${VERSION}

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

for (( i=0; i<${size}; i++ ));
  do
    if [ ${nodes[${i}]} == masternode ]
      then
        sudo docker create\
          --name couchdb${masternode}\
          -p ${masterport}:5984\
          -v /opt/couchdb/master/data:/opt/couchdb/data\
          --env COUCHDB_USER=${user}\
          --env COUCHDB_PASSWORD=${pass}\
          --env COUCHDB_SECRET=${cookie}\
          --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${masternode}\""\
          couchdb:${VERSION}
      else
        sudo docker create\
          --name couchdb${nodes[${i}]}\
          -p ${ports[${i}]}:5984\
          -v /opt/couchdb/worker${indexdb[${i}]}/data:/opt/couchdb/data\
          --env COUCHDB_USER=${user}\
          --env COUCHDB_PASSWORD=${pass}\
          --env COUCHDB_SECRET=${cookie}\
          --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${nodes[${i}]}\""\
          couchdb:${VERSION}
    fi
done

echo "== done creating docker =="

# put in const in docker container IDs
declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

# start the containers
for cont in "${conts[@]}"; do sudo docker start ${cont}; done

echo "== done starting docker =="

sleep 10

# setup the couchdb cluster
for (( i=0; i<${sizeworker}; i++ ));
do
    curl -XPOST "http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"${otherports[${i}]}\",\
             \"remote_node\": \"${othernodes[${i}]}\", \"node_count\": \"$(echo ${nodes[@]} | wc -w)\",\
             \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done

for (( i=0; i<${sizeworker}; i++ ));
do
    curl -XPOST "http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"${othernodes[${i}]}\",\
             \"port\": \"${otherports[${i}]}\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
done

sleep 5

# send empty request to avoid error message when finishing the cluster setup
curl -XGET "http://${user}:${pass}@${masternode}:15984/"

curl -XPOST "http://${user}:${pass}@${masternode}:15984/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"

sleep 5

# check whether cluster configuration is finished
for (( i=0; i<${sizeworker}; i++ )); do  curl -X GET "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_membership"; done

# add database to check whether it is created in other nodes as well
curl -XPUT "http://${user}:${pass}@${masternode}:${masterport}/testdb"
for (( i=0; i<${sizeworker}; i++ )); do  curl -X GET "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_all_dbs"; done

# =================================================================================================

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
