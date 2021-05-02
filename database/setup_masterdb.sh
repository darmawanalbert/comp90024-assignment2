# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

# declare variables for the couchdb cluster setup
export declare -a nodes=(45.113.234.156 45.113.234.166)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export declare -a ports=(15984 25984)
export masterport=`echo ${ports} | cut -f1 -d' '`
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export declare -a otherports=`echo ${ports[@]} | sed s/${masterport}//`
export declare -a indexdb=(0 1)
export size=${#nodes[@]}
export sizeworker=${#othernodes[@]}
export mastervolume='/opt/couchdb/master/data:/opt/couchdb/data'
export user='admin'
export pass='admin'
export VERSION='latest'
export cookie='a192aeb9904e6590849337933b000c99'

# pull from dockerhub official couchdb
sudo docker pull couchdb:${VERSION}
sudo docker network create --driver bridge couch

# create docker container
# stops and removes the docker if already exist

if [ ! -z $(sudo docker ps --all --filter "name=mastercouchdb" --quiet) ]
  then
    sudo docker stop mastercouchdb
    sudo docker rm mastercouchdb
fi

sudo docker create\
  --name mastercouchdb\
  --net=couch\
  --hostname couchdb@${masternode}\
  -p ${masterport}:5984\
  -p 4369:4369\
  -p 9100:9100\
  -v /opt/couchdb/master/data:/opt/couchdb/data\
  -v /tmp/my.cookie:/opt/couchdb/.erlang.cookie\
  --env NODENAME=couchdb@${masternode}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env COUCHDB_SECRET=${cookie}\
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${masternode}\"\
  -kernel \"inet_dist_listen_min 9100\" -kernel \"inet_dist_listen_max 9100\""\
  couchdb:${VERSION}

# for node in "${nodes[@]}"
#   do
#     if [ ! -z $(sudo docker ps --all --filter "name=couchdb${node}" --quiet) ] 
#        then
#          sudo docker stop $(sudo docker ps --all --filter "name=couchdb${node}" --quiet) 
#          sudo docker rm $(sudo docker ps --all --filter "name=couchdb${node}" --quiet)
#     fi
# done

# for (( i=0; i<${size}; i++ ));
#   do
#     if [ ${nodes[${i}]} == masternode ]
#       then
#         sudo docker create\
#           --name couchdb${masternode}\
#           -p ${masterport}:5984\
#           -v /opt/couchdb/master/data:/opt/couchdb/data\
#           --env COUCHDB_USER=${user}\
#           --env COUCHDB_PASSWORD=${pass}\
#           --env COUCHDB_SECRET=${cookie}\
#           --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${masternode}\""\
#           couchdb:${VERSION}
#       else
#         sudo docker create\
#           --name couchdb${nodes[${i}]}\
#           -p ${ports[${i}]}:5984\
#           -v /opt/couchdb/worker${indexdb[${i}]}/data:/opt/couchdb/data\
#           --env COUCHDB_USER=${user}\
#           --env COUCHDB_PASSWORD=${pass}\
#           --env COUCHDB_SECRET=${cookie}\
#           --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${nodes[${i}]}\""\
#           couchdb:${VERSION}
#     fi
# done

echo "== done creating docker =="

# put in const in docker container IDs
# declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

# start the containers
# for cont in "${conts[@]}"; do sudo docker start ${cont}; done
sudo docker start mastercouchdb

echo "== done starting docker =="

sleep 10

sudo docker exec mastercouchdb bash -c "echo \"-setcookie \"${cookie}\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec mastercouchdb bash -c "echo \"-name \"couchdb@${masternode}\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec mastercouchdb bash -c "echo \"-kernel \"inet_dist_listen_min\" \"9100\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec mastercouchdb bash -c "echo \"-kernel \"inet_dist_listen_max\" \"9100\"\" >> /opt/couchdb/etc/vm.args"

sudo docker restart mastercouchdb

sleep 15

# setup the couchdb cluster
echo "== Enable cluster setup =="
for (( i=0; i<${size}; i++ )); do
    curl -X PUT "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_node/_local/_config/admins/${user}" -d "\"${pass}\""
    sleep 3
    curl -X PUT "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_node/_local/_config/chttpd/bind_address" -d '"0.0.0.0"'
    sleep 2
done

echo "== Add nodes to cluster =="
for (( i=0; i<${size}; i++ )); do
    if [ "${nodes[${i}]}" != "${masternode}" ]; then
        curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup \
            -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": ${ports[${i}]}, \"node_count\": \"${size}\", \
            \"remote_node\": \"${nodes[${i}]}\", \"remote_current_user\": \"${user}\", \"remote_current_password\": \"${pass}\"}"
        curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup \
            -d "{\"action\": \"add_node\", \"host\":\"${nodes[${i}]}\", \"port\": ${ports[${i}]}, \"username\": \"${user}\", \"password\":\"${pass}\"}"
    fi
done

# for (( i=0; i<${sizeworker}; i++ ));
#   do
#     curl -XPOST "http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup"\
#       --header "Content-Type: application/json"\
#       --data "{\"action\":\"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
#              \"username\":\"${user}\", \"password\":\"${pass}\", \"port\":\"${otherports[${i}]}\",\
#              \"remote_node\":\"${othernodes[${i}]}\", \"node_count\":\"$(echo ${nodes[@]} | wc -w)\",\
#              \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
#     curl -XPOST "http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup"\
#       --header "Content-Type: application/json"\
#       --data "{\"action\":\"add_node\", \"host\":\"${othernodes[${i}]}\",\
#              \"port\":\"${otherports[${i}]}\", \"username\":\"${user}\", \"password\":\"${pass}\"}"
# done

sleep 10

# send empty request to avoid error message when finishing the cluster setup
curl -XGET "http://${user}:${pass}@${masternode}:${masterport}/"

sleep 5

curl -XPOST "http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"

sleep 5

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
