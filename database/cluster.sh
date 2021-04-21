curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "node_count":"3"}'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "port": 5984, "node_count": "3", "remote_node": "db-worker", "remote_current_user": "admin", "remote_current_password": "admin" }'
curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "add_node", "host":"db-worker", "port": "5984", "username": "admin", "password":"admin"}'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "finish_cluster"}'

curl -X PUT http://admin:admin@127.0.0.1:5984/testdb

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_replicator -d '{"source": "http://admin:admin@127.0.0.1:5984/testdb","target":  "http://admin:admin@db-worker:5984/testdb","create_target":  true,"continuous": true}'