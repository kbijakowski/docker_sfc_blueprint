# Docker containers service chain example

## Overview

Purpose of this example is to show how TOSCA-based orchestration may be used to provisioning of virtualized network services chain in non-specialized environment.

In this example Cloudify orchestration was used.
Repository consists of Cloudify services descriptors (blueprints).

As result of execution of this example you will have fully-functional service chain with 3 services.

![](https://user-images.githubusercontent.com/20417307/50763921-83010f80-1271-11e9-9455-cf0f050a14ea.jpg)

All services and infrastructure elements are run as docker containers.
During example execution 5 docker containers will be created:
* **host** - container to which we can attach terminal session and check connectivity with server through service chain 
* **server** - container running 2 python SimpleHTTPServers on ***8080*** and ***8181*** ports
* **vRouter** - 1st service - container acts as virtual router
* **vFirewall** - 2nd service - container using iptables to drop HTTP traffic on ***8181*** port 
* **vURLFilter** - 3rd service - container running ***squid3***. Should restrict access to HTTP server on ***8080*** port 

Also connections between containers are made using standard docker networks (bridge) API. 
Orchestrator uses docker REST API to provision all elements and configuration.

![](https://user-images.githubusercontent.com/20417307/50763927-8399a600-1271-11e9-8fba-c0ce3b860d2c.jpg)

To steer traffic between services one container running Open vSwitch is used.
This container is connected by docker networks with each of containers.

In OvS container one ***main*** OpenFlow bridge has been defined - it is ***br0***.
Its role is to steer traffic between *input* (host container), *output* (server container) and *endpoints* (additional OpenFlow bridges dedicated to plug services in).   

***Endpoint*** bridge can be considered and **connector** to which you can plug your own service. 
Each of ***endpoint*** OpenFlow bridges: ***br1***, ***br2*** and ***br3*** have initially 2 *patch* interfaces with peers defined in *main* brigge interfaces.
In initial mode it forwards traffic between its patch interfaces - this behaviour enables traffic to be forwarded without any service plugged.
During service blueprint installation new service is plugged to endpoint bridge.
To new interfaces connected to *endpoint* bridge and appropiate docker networks are created.
Installation of *service blueprint* reconfigures also OpenFlow flows defined in *endpoint* bridge to forward traffic between patch interfaces connected to *br0* and external interfaces connected to service networks.
During service blueprint uninstallation external interfaces are removed and flows are "reverted" to forward traffic again between patch interfaces. 
Purpose of introducing this kind of architecture was to provide additional abstraction layer - we can simply plug and unplug service without need of main bridge flows reconfiguration.
 
Each service container has interfaces to 2 networks: "input" chain network and "output" chain network.
 
## Implementation

![](https://user-images.githubusercontent.com/20417307/50763920-83010f80-1271-11e9-9216-ab08958341a7.jpg)

Solution has been implemented as set o 3 blueprints:

* **main infrastructure blueprint** - responsible for provisioning of:
    * *host*, *server* and *ovs* containers
    * docker newtorks between containers
    * *main OpenFlow bridge (br0)* on ovs container
    * proper openflow interfaces connected to *br0*
    * flows on *br0*
    
    **It also uses** ***endpoint infrastructure blueprint*** **to provision 3 endpoint blueprint** 
* **endpoint infrastructure blueprint** - responsible for provisioning of:
    * *endpoint OpenFlow bridge* on ovs container
    * proper openflow interfaces connected to *endpoint bridge*
    * flows on *endpoint bridge*
* **service blueprint** - responsible for provisioning of:
    * service container
    * simple service configuration
    * "input" and "output" docker newtorks dedicated for each service
    * proper openflow interfaces connected to *endpoint bridge*
    * flows reconfiguration on *endpoint bridge*

***endpoint infrastructure blueprint*** must be uploaded first on Cloudify Manager.
It is used (read and executed) by ***main infrastructure blueprint*** during its installation.  


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