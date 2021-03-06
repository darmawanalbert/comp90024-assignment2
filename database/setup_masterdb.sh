# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

source constants.sh

# declare variables for the couchdb cluster setup
export declare -a nodes=(${INSTANCE4} ${INSTANCE3})
export masternode=`echo ${nodes} | cut -f1 -d' '`
export declare -a ports=(15984 25984)
export masterport=`echo ${ports} | cut -f1 -d' '`
export declare -a indexdb=(0 1)
export declare -a dblist=(comp90024_tweet_harvest comp90024_tweet_search\
                          comp90024_lda_scoring comp90024_aurin_statistics)
export declare -a replist=(harvest_rep search_rep lda_scoring_rep aurin_stats_rep)
export size=${#nodes[@]}
export dbsize=${#dblist[@]}
export user='admin'
export pass='admin'
export VERSION='latest'
export cookie='0c16e9f0bd3fc12edd83516529995817'

# pull from dockerhub official couchdb
echo "===== docker pull from official couchdb ====="
sudo docker pull couchdb:${VERSION}
sudo docker network create --driver bridge couch
echo "===== done pulling ====="
echo " "

# create docker container
# stops and removes the docker if already exist
echo "===== creating docker couchdb ====="

if [ ! -z $(sudo docker ps --all --filter "name=mastercouchdb" --quiet) ]
  then
    sudo docker stop mastercouchdb
    sudo docker rm mastercouchdb
fi

sudo docker create\
  --name mastercouchdb\
  --network-alias couchdb@${masternode}\
  --hostname couchdb@${masternode}\
  -p ${masterport}:5984\
  -p 5986:5986\
  -p 4369:4369\
  -p 9100:9100\
  -v /opt/couchdb/master/data:/opt/couchdb/data\
  --env NODENAME=couchdb@${masternode}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env COUCHDB_SECRET=${cookie}\
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${masternode}\"\
  -kernel \"inet_dist_listen_min 9100\" -kernel \"inet_dist_listen_max 9100\""\
  couchdb:${VERSION}

#   --net=couch\

echo "===== done create ====="
echo " "

echo "===== starting docker couchdb ====="
# start the container
sudo docker start mastercouchdb

sleep 10

sudo docker cp default.ini mastercouchdb:/opt/couchdb/etc/
sudo docker cp local.ini mastercouchdb:/opt/couchdb/etc/
sudo docker exec mastercouchdb bash -c "sed -i '/-name couchdb@couchdb@${masternode}/d' /opt/couchdb/etc/vm.args"
sudo docker exec mastercouchdb bash -c "echo \"-name \"couchdb@${masternode}\"\" >> /opt/couchdb/etc/vm.args"
sudo docker exec mastercouchdb bash -c "echo \"-setcookie \"${cookie}\"\" >> /opt/couchdb/etc/vm.args"
# sudo docker exec mastercouchdb bash -c "echo \"-kernel \"inet_dist_listen_min\" \"9100\"\" >> /opt/couchdb/etc/vm.args"
# sudo docker exec mastercouchdb bash -c "echo \"-kernel \"inet_dist_listen_max\" \"9100\"\" >> /opt/couchdb/etc/vm.args"

sudo docker restart mastercouchdb

echo "===== docker started ====="
sleep 15
echo " "

# setup the couchdb cluster
echo "===== enable cluster setup ====="
for (( i=0; i<${size}; i++ )); do
    curl -X PUT http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_node/_local/_config/admins/${user} -d "\"${pass}\""
    sleep 3
    curl -X PUT http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_node/_local/_config/chttpd/bind_address -d '"0.0.0.0"'
    sleep 2
    curl -X POST -H "Content-Type: application/json" http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_cluster_setup \
        -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${pass}\", \
        \"node_count\":\"${size}\"}"
    curl -X GET "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_membership"
    sleep 2

done

echo "===== Add nodes to cluster ====="
for (( i=0; i<${size}; i++ )); do
    if [ "${nodes[${i}]}" != "${masternode}" ]; then
        curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup \
            -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${pass}\", \
            \"port\": ${ports[${i}]}, \"node_count\": \"${size}\", \"remote_node\": \"http://${nodes[${i}]}\", \"remote_current_user\": \"${user}\", \
            \"remote_current_password\": \"${pass}\"}"
        curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup \
            -d "{\"action\": \"add_node\", \"host\":\"${nodes[${i}]}\", \"port\": ${ports[${i}]}, \"username\": \"${user}\", \
            \"password\":\"${pass}\"}"
    fi
done

sleep 10

# send empty request to avoid error message when finishing the cluster setup
curl -XGET "http://${user}:${pass}@${masternode}:${masterport}/"

sleep 5

curl -XPOST "http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"

echo "===== done setup cluster ====="
echo " "
sleep 5

echo "===== perform checking on the couchdb setup ======"
# check whether cluster configuration is finished
for (( i=0; i<${size}; i++ )); do curl -X GET "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_membership"; done

# add database in dblist and check whether it is created in other nodes as well
for db in ${dblist[@]}
do
    curl -X PUT "http://${user}:${pass}@${masternode}:${masterport}/${db}"
done
for (( i=0; i<${size}; i++ )); do  curl -X GET "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_all_dbs"; done

echo "===== mastercouchdb setup finished ======"
echo " "

echo "===== setup replicator ====="
for (( i=0; i<${size}; i++ )); do
    declare workercurl=http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}
    if [ "${nodes[${i}]}" != "${masternode}" ]; then
        for (( i=0; i<${dbsize}; i++ )); do
            curl -X POST -H "Content-Type: application/json" http://${user}:${pass}@${masternode}:${masterport}/_replicator \
                -d "{\"_id\": \"${replist[${i}]}\", \"source\": \"http://${user}:${pass}@${masternode}:${masterport}/${dblist[${i}]}\", \
                \"target\": \"${workercurl}/${dblist[${i}]}\", \"create_target\": true, \
                \"continuous\": true}"
        done
    fi
done