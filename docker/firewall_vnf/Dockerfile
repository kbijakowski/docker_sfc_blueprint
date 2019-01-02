FROM ianneub/network-tools

RUN apt install -y iptables tcpdump

ENTRYPOINT iptables -A FORWARD -p tcp -m state --state NEW -m tcp --dport 8181 -j DROP && /bin/bash
