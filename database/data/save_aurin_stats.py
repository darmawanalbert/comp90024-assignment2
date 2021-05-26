"""
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
"""

import json
import argparse
import requests
import hashlib

# Argparse build
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fileaurin", help="Type your aurin statistics json file directory")
args = parser.parse_args()

AURIN_FILE = args.fileaurin

# Hashing md5 in generating the _id using file name as the string
hash_aurin = hashlib.md5()
hash_aurin.update(AURIN_FILE[:-5].encode('utf-8'))

AURIN_FILE_ID = hash_aurin.hexdigest()

# Loading the data from the file to dictionary
with open(AURIN_FILE, 'r') as af:
    aurin_json = json.load(af)
    aurin_dict = dict(aurin_file_name=AURIN_FILE, aurin_doc=aurin_json)

# Store the data using PUT method
headers = {"content-type": "application/json"}
url = "http://admin:admin@45.113.234.151:15984/comp90024_aurin_statistics/" + AURIN_FILE_ID
data = json.dumps(aurin_dict).encode('utf-8')

req_status = requests.put(url, data=data, headers=headers)
print(req_status)