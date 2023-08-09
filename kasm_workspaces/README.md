## Workflow
1. `Code` in dockerfile-* and in src directory
    - add code for new tools
    - add support files to src/ubuntu/install, check [Kasm](https://github.com/kasmtech/workspaces-images.git)
2. `Build` the dockerfile-* file
```bash
docker build -t devops/kasm-workspaces:1.0 -f dockerfile-csse-nighthawk-ubuntu-jammy-desktop .
```
3. `Push` the docker files
```bash
docker push
```
4. `Test` the on Kasm (kasm100.nighthawkcodingsociety.com)
    - install workspace from registry
    - run workpace

## Registry Requirements 
The registry has an instance of the devOps kasm_workspaces.
- Location: [https://nighthawkcoders.github.io/kasm_registry/1.0/](https://nighthawkcoders.github.io/kasm_registry/1.0/)