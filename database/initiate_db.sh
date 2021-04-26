#!/usr/bin/env bash

echo "== Set variables =="
export declare -a nodes=(115.146.95.84 45.113.235.136 45.113.233.153)
export declare -a ports=(5984 15984 25984)
export masternode=115.146.95.84
export masterport=5984
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export declare -a otherports=`echo ${ports[@]} | sed s/${masterport}//`
export size=${#nodes[@]}
export user=admin
export pass=admin

echo "== Start the containers =="
sudo docker-compose up -d

sleep 30

# # put in const in docker container IDs
# declare -a conts=(`sudo docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

# # start the containers
# for cont in "${conts[@]}"; do sudo docker start ${cont}; done

# # sleep for 10s after starting
# sleep 10

# # setup the couchdb cluster
# for node in ${othernodes}
# do
#     curl -XPOST "http://${user}:${pass}@${masternode}:${masterport}/_cluster_setup" \
#       --header "Content-Type: application/json"\
#       --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
#              \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"${otherports}\",\
#              \"remote_node\": \"${node}\", \"node_count\": \"$(echo ${nodes[@]} | wc -w)\",\
#              \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
# done

# for node in ${othernodes}
# do
#     curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
#       --header "Content-Type: application/json"\
#       --data "{\"action\": \"add_node\", \"host\":\"${node}\",\
#              \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
# done

echo "== Enable cluster setup =="
for (( i=0; i<${size}; i++ )); do
  curl -X POST "http://${user}:${pass}@localhost:${ports[${i}]}/_cluster_setup" -H 'Content-Type: application/json' \
    -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${pass}\", \"node_count\":\"${size}\"}"
done

sleep 10

echo "== Add nodes to cluster =="
for (( i=0; i<${size}; i++ )); do
  if [ "${nodes[${i}]}" != "${master_node}" ]; then
    curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@127.0.0.1:${master_port}/_cluster_setup \
      -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": 5984, \"node_count\": \"${size}\", \
           \"remote_node\": \"${nodes[${i}]}\", \"remote_current_user\": \"${user}\", \"remote_current_password\": \"${pass}\"}"
    curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@127.0.0.1:${master_port}/_cluster_setup \
      -d "{\"action\": \"add_node\", \"host\":\"${nodes[${i}]}\", \"port\": 5984, \"username\": \"${user}\", \"password\":\"${pass}\"}"
  fi
done

sleep 10

curl -X POST "http://${user}:${pass}@localhost:${master_port}/_cluster_setup" -H 'Content-Type: application/json' -d '{"action": "finish_cluster"}'

curl http://${user}:${pass}@localhost:${master_port}/_cluster_setup

for port in "${ports[@]}"; do  curl -X GET http://${user}:${pass}@localhost:${port}/_membership; done