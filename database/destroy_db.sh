# COMP90024 Team 1
# Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
# Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
# I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
# Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au

# Use this file to destroy db

# Change the constants to the instance you wish to destroy
source constants.sh
export node=${INSTANCE4}
export dockername=mastercouchdb

# Disconnecting network
sudo docker network disconnect couchdb@${node} dockername
sudo docker network rm couchdb@${node}

# Stopping and removing CouchDB docker
sudo docker stop dockername
sudo docker rm dockername