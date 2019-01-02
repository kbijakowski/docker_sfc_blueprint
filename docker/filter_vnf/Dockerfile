FROM ianneub/network-tools

RUN apt install -y iptables tcpdump
RUN apt install -y squid
RUN echo banned > /etc/squid3/banned-urls
RUN sed -i 's/http_port 3128/http_port 3128 transparent/g' /etc/squid3/squid.conf
RUN sed -i '/INSERT YOUR OWN RULE/a http_access deny banned-urls' /etc/squid3/squid.conf
RUN sed -i '/INSERT YOUR OWN RULE/a acl banned-urls url_regex "/etc/squid/banned-urls"' /etc/squid3/squid.conf

ENTRYPOINT iptables -t nat -A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-port 3128 && squid3 && /bin/bash
