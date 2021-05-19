# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

import couchdb
import os

#Instance 4 test
#ADDRESS='http://admin:admin@45.113.235.136:15984/'
ADDRESS = os.environ.get('ADDRESS') if os.environ.get('ADDRESS') != None else "http://admin:admin@45.113.235.136:15984"

# A class to create a database instance
# The instance will automatically connect to the CouchDB hosted in MRC
class DB_Utils():
    def __init__(self):
        try:
            self.server = couchdb.Server(ADDRESS)
            print("Connection to CouchDB successful....")
        except Exception as e:
            print(e)
            print('Connected to CouchDB failed....')
    
    #A function to create a connection with a designated database
    def db_connect(self,database):
        try:
            self.db = self.server[database]
            print(str(database)+' Database Found....')
        
        #Will be triggered when the database is not found in the CouchDB
        #An attempt of creating the database will be executed 
        except couchdb.http.ResourceNotFound:
            print(str(database)+" Not Found....")
            print("Try to create new database named: "+str(database))
            self.server.create(database)
            self.db = self.server[database]
        except Exception as e:
            print('error here')
            print(e)
            exit(-1)
    
    #A function to save a record into the designated database
    def save(self,database,record):
        try:
            self.db.save(record)
            print(record)
            print('Saved successfully')
        except Exception as e:
            print('Failed to save record in the database')
            print(e)
