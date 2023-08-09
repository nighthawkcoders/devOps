## Workflow
1. `Code` in dockerfile-* and in src directory
    - add code for new tools
    - add support files to src/ubuntu/install, check [Kasm](https://github.com/kasmtech/workspaces-images.git)
2. `Build` the dockerfile-* file

```bash
# clean up docker often, before a new run is best
docker image prune  
docker build -t devops/csse-kasm-workspaces:1.0 -f dockerfile-csse-nighthawk-ubuntu-jammy-desktop .
````

```bash
# This can take a long time, see time!!!
[+] Building 872.6s (15/15) FINISHED                                                                            
 => [internal] load build definition from dockerfile-csse-nighthawk-ubuntu-jammy-desktop-agupta            0.0s
 => => transferring dockerfile: 2.11kB                                                                     0.0s
 => [internal] load .dockerignore                                                                          0.0s
 => => transferring context: 2B                                                                            0.0s
 => [internal] load metadata for docker.io/kasmweb/core-ubuntu-focal:1.13.1                                2.6s
 => [ 1/10] FROM docker.io/kasmweb/core-ubuntu-focal:1.13.1@sha256:5c2f1bbe9bcc679ddcdf73e21f8ce9d4214cfb  0.0s
 => [internal] load build context                                                                          0.0s
 => => transferring context: 15.66kB                                                                       0.0s
 => CACHED [ 2/10] WORKDIR /home/kasm-default-profile                                                      0.0s
 => CACHED [ 3/10] COPY ./src/ubuntu/install /dockerstartup/install                                        0.0s
 => CACHED [ 4/10] RUN   for SCRIPT in tools/install_tools.sh                   chrome/install_chrome.sh   0.0s
 => [ 5/10] RUN cd /tmp/ &&     wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64  123.9s
 => [ 6/10] RUN echo 'export PATH="/opt/anaconda3/bin:$PATH"' >> /etc/bash.bashrc &&     /opt/anaconda3  573.9s
 => [ 7/10] RUN chown 1000:0 /home/kasm-default-profile                                                    0.3s 
 => [ 8/10] RUN /dockerstartup/set_user_permission.sh /home/kasm-default-profile                           1.2s 
 => [ 9/10] WORKDIR /home/kasm-user                                                                        0.0s 
 => [10/10] RUN mkdir -p /home/kasm-user && chown -R 1000:0 /home/kasm-user                                0.2s 
 => exporting to image                                                                                   170.3s 
 => => exporting layers                                                                                  170.2s 
 => => writing image sha256:d9c1fd0c858f8d6e43eea6d4ce52540e718374da85e8774c05bd2d6f334d374c               0.0s
 => => naming to docker.io/devops/csse-kasm-workspaces:1.0     
docker build -t devops/kasm-workspaces:1.0 -f dockerfile-csse-nighthawk-ubuntu-jammy-desktop .
```
3. `Push` the docker files

```bash
# You need to setup something like https://hub.docker.com/repository/docker/nighthawkcoders/kasm_workspaces/general
docker push nighthawkcoders/kasm_workspaces:1.0
```

4. `Test` the on Kasm (kasm100.nighthawkcodingsociety.com)
    - install workspace from registry
    - run workpace

## Registry Requirements 
The registry has an instance of the devOps kasm_workspaces.
- Location: [https://nighthawkcoders.github.io/kasm_registry/1.0/](https://nighthawkcoders.github.io/kasm_registry/1.0/)