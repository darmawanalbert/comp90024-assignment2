# create db master
docker run --name db-master -p 15984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin -e NODENAME=db-master -v /couchmasterdata:/opt/couchdb/data  -d couchdb:latest

# create worker master
docker run --name db-worker -p 25984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin -e NODENAME=db-worker -v /couchworkerdata:/opt/couchdb/data  -d couchdb:latest

# setup couchdb network
docker network create couchdbnet
docker network connect couchdbnet db-master
docker network connect couchdbnet db-worker

# sleep 5s
sleep 5

# create database
curl -X PUT http://admin:admin@127.0.0.1:15984/testdb
curl -X PUT http://admin:admin@127.0.0.1:15984/twitter_db_test

# setup cluster
curl -X PUT http://admin:admin@127.0.0.1:15984/_users

curl -X PUT http://admin:admin@127.0.0.1:15984/_replicator

curl -X PUT http://admin:admin@127.0.0.1:15984/_global_changes

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "node_count":"3"}'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "port": 5984, "node_count": "3", "remote_node": "db-worker", "remote_current_user": "admin", "remote_current_password": "admin" }'
curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "add_node", "host":"db-worker", "port": "5984", "username": "admin", "password":"admin"}'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_cluster_setup -d '{"action": "finish_cluster"}'

# setup replicator
curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:15984/_replicator -d '{"_id": "my_rep","source": "http://admin:admin@localhost:5984/testdb","target":  "http://admin:admin@db-worker:5984/testdb","create_target":  true,"continuous": true}'

# temp
curl -X GET http://admin:admin@127.0.0.1:15984/_all_dbs

curl -X GET http://admin:admin@127.0.0.1:15984/_scheduler/docs/_replicator/my_rep