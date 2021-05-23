import couchdb

ADDRESS='http://admin:admin@45.113.235.136:15984'
DB_NAME = 'test_new1'

server = couchdb.Server(ADDRESS)

print(server[DB_NAME])