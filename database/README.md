# COMP90024 Team 1

Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au<br />
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au<br />
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au<br />
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au<br />
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au<br />

-------------------------------------

# Database CouchDB Setup and Maintenance
## Prerequisites
- Docker
- npm
- node.js
- Running instances or VM

## Setup
1. Run the `setup_masterdb.sh` and `setup_workerdb1.sh` on your allocated instances
2. If you wish to change the port, change the port inside the file. Currently used ports are 15984 for server and 25984 for worker
3. Run `npm install` with optional admin privileges
4. Run `compile_views.sh` to push views to database

## Starting and stopping CouchDB
Just run `sudo docker start ${DOCKERNAME}` to start CouchDB and `sudo docker stop ${DOCKERNAME}` to stop CouchDB on each instances

## Destroy database
Just run `destroy_db.sh` with specified docker name to be edited inside the file

## Backup
To backup CouchDB data, use the `couchdb-dump.sh` file. For more instructions, please read inside the file.