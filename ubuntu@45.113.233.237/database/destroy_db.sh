docker network disconnect couchdbnet db-worker
docker network disconnect couchdbnet db-master
docker network rm couchdbnet

# stop
docker container stop db-worker db-master

# remove
docker container rm db-worker db-master