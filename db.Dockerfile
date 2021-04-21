FROM couchdb:latest

COPY database/cluster.sh /opt/couchdb/etc/

RUN chmod +x /opt/couchdb/etc/cluster.sh

EXPOSE 5984 4369 9100

ENTRYPOINT ["/opt/couchdb/etc/cluster.sh"]

CMD ["/opt/couchdb/bin/couchdb"]