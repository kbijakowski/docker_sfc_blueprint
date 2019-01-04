#!/bin/bash

DOCKERFILES_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd $DOCKERFILES_PATH/client && ./build.sh
cd $DOCKERFILES_PATH/filter_vnf && ./build.sh
cd $DOCKERFILES_PATH/firewall_vnf && ./build.sh
cd $DOCKERFILES_PATH/router_vnf && ./build.sh
cd $DOCKERFILES_PATH/server && ./build.sh
