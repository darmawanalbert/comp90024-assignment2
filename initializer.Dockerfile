FROM curlimages/curl

COPY database/cluster.sh /opt/cluster.sh

CMD ["/bin/sh","-c","/opt/cluster.sh"]