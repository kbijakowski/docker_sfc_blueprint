1. Execute:

    ```
        docker ps -a
        docker network list
    ```

2. Execute:
    ```
        cfy blueprints upload infrastructure_endpoint-blueprint.yaml -b cfy_lab_infrastructure_endpoint
    ```

3. Execute:
    ```
        cfy install infrastructure_main-blueprint.yaml -i inputs/infrastructure_main-inputs.yaml -b cfy_lab_infrastructure
    ```
    
4. Execute:

    ```
        cfy deployments outputs cfy_lab_infrastructure
    ```

5. Execute command from output *ping_check_command* 

6. Execute:
    ```
        docker ps -a
        docker network list
    ```
    
7. Execute:     
    ```
        cfy uninstall cfy_lab_infrastructure
    ```

8. Execute:     
    ```
        cfy blueprints delete cfy_lab_infrastructure_endpoint
    ``` 
    
9. Execute:
    ```
        docker ps -a
        docker network list
    ```