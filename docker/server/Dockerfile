FROM ianneub/network-tools

RUN apt update && apt upgrade -y
RUN apt install -y tcpdump
RUN apt install -y python2.7

ENTRYPOINT python2.7 -m SimpleHTTPServer 8080 & python2.7 -m SimpleHTTPServer 8181 & /bin/bash
