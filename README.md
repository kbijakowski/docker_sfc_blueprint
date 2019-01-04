# Docker containers service chain example

## Overview

TBD

## Implementation

TBD

## Prerequisites

* **Docker**

    You need to install docker to run this example. 
    Blueprints have been tested on ***docker v.1.13.1***.
    
* **Docker REST API expose**

    Docker REST API should be reachable for Cloudify Manager, so you need to expose it on localhost.
    Exposing process is described here: 
    
    https://success.docker.com/article/how-do-i-enable-the-remote-api-for-dockerd
    
    Blueprints have been tested using ***docker REST API v.1.26 and v.1.38***.
    
* **Docker images**

    5 custom images are used in this example. There are:
    * ***cfy_lab_docker_sfc/server***
    * ***cfy_lab_docker_sfc/firewall_vnf***
    * ***cfy_lab_docker_sfc/filter_vnf***
    * ***cfy_lab_docker_sfc/client***
    * ***cfy_lab_docker_sfc/router_vnf***
    
    Before start you need to build them:
    
    ```bash
    ./docker/build_all.sh
    ```
    
    Also one image needs to be pulled:
    * ***socketplane/openvswitch***
    
    It is good idea to pull it once before start:
    
    ```bash
    docker pull socketplane/openvswitch
    ```

* **Container with Cloudify Manager**

    To run this example you need to have an instance of Cloudify Manger.
    
    It may be simply run on docker usign this command:
    
    ```bash
    sudo docker run --name cfy_manager_local -d --restart unless-stopped -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --security-opt seccomp:unconfined --cap-add SYS_ADMIN -p 80:80 -p 8000:8000 cloudifyplatform/premium
    ```

    Blueprints have been tested using ***Cloudify Manager v.4.5***.
    
* **cloudify-utilities-plugin v.1.12.0**

    Last required preparation step is to upload ***cloudify-utilities-plugin*** into Cloudify Manager:

    ```bash
    cfy plugins upload https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/1.12.0/cloudify_utilities_plugin-1.12.0-py27-none-linux_x86_64-centos-Core.wgn -y https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/1.12.0/plugin.yaml
    ```

## Demo execution

Before start - check if there are no existing Docker resources. Execute:

```bash
docker ps -a
```

You should observe the only one container with Cloudify Manager is running:

```bash
3252d0d3b35b        cloudifyplatform/premium    "/bin/bash -c 'exe..."   5 weeks ago         Up 9 minutes                22/tcp, 443/tcp, 0.0.0.0:80->80/tcp, 0.0.0.0:8000->8000/tcp, 5671-5672/tcp, 0.0.0.0:53333->53333/tcp   cfy_manager_local
```

Then check existing Docker networks:

```bash
docker network list
```

No networks with prefix *cfy_lab* should be present:

```bash
NETWORK ID          NAME                     DRIVER              SCOPE
f6459a81cb93        bridge                   bridge              local
07c9ed0b8bd5        host                     host                local
80089a4cbcba        none                     null                local
```

#### Stage 1 - chain infrastructure installation

Purpose of this step execution is to create SFC infrastructure - all things required to start inserting services into chain, lie:
* containers with host, OpenvSwitch and server
* networks connecting host with OvS and OvS with server
* proper network interfaces
* OvS bridges
* OvS flows

When blueprints installation will be completed successfully, you should have ready SFC setup to which 3 services may be plugged.
You should be able to access / ping server from the host, but traffic will be forwarded only through OvS bridges (no services containers plugged).

**[TODO] IMAGE**  

1. Upload ***infrastructure-endpoint blueprint***. It will be used in step 2 by *infrastructure-main blueprint*. Execute:
    ```
    cfy blueprints upload infrastructure_endpoint-blueprint.yaml -b cfy_lab_infrastructure_endpoint
    ```

2. Install ***infrastructure-main blueprint***
    ```
    cfy install infrastructure_main-blueprint.yaml -i inputs/infrastructure_main-inputs.yaml -b cfy_lab_infrastructure
    ```
    
3. Execute:

    ```
    cfy deployments outputs cfy_lab_infrastructure
    ```

4. Execute command from output *ping_check_command* 

5. Execute:
    ```
        docker ps -a
        docker network list
    ```

#### Stage 2 - vRouter service insertion

#### Stage 3 - vFirewall service insertion

#### Stage 4 - vURLFilter service insertion

#### Stage 5 - single service removal (vFirewall)

#### Stage 6 - service cleanup

#### Stage 7 - chain infrastructure uninstallation
    
1. Execute:     
    ```
        cfy uninstall cfy_lab_infrastructure
    ```

2. Execute:     
    ```
        cfy blueprints delete cfy_lab_infrastructure_endpoint
    ``` 
    
3. Execute:
    ```
        docker ps -a
        docker network list
    ```