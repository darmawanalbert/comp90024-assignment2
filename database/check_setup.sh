# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

# declare constant
export declare -a nodes=(45.113.234.156 45.113.234.166)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export declare -a ports=(15984 25984)
export masterport=`echo ${ports} | cut -f1 -d' '`
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export declare -a otherports=`echo ${ports[@]} | sed s/${masterport}//`
export declare -a indexdb=(0 1)
export size=${#nodes[@]}
export sizeworker=${#othernodes[@]}
export user='admin'
export pass='admin'

# check whether cluster configuration is finished
for (( i=0; i<${size}; i++ )); do  curl -X GET "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_membership"; done

# add harvest database and check whether it is created in other nodes as well
curl -XPUT "http://${user}:${pass}@${masternode}:${masterport}/tweet_harvest"
for (( i=0; i<${size}; i++ )); do  curl -X GET "http://${user}:${pass}@${nodes[${i}]}:${ports[${i}]}/_all_dbs"; done