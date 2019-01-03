# Docker containers service chain example

## Overview

TBD

## Prerequisites

1. Docker

    Tested on ...

2. Container with Cloudify Manager

    Tested on ...

3. Docker API expose

4. Images

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

1. Execute:
    ```
        cfy blueprints upload infrastructure_endpoint-blueprint.yaml -b cfy_lab_infrastructure_endpoint
    ```

2. Execute:
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