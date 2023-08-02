## Developer Operations for Nighthawk Students and Infrastructure
TBD Runtime link: https://devops.nighthawkcodingsociety.com/

### Primary way to get started
> Quick steps that can be used with MacOS or WSL; this uses Python 3.9 or later as a prerequisite.

- Open a Terminal, clone project and cd to project area

```bash
mkdir ~/vscode; cd ~/vscode

git clone https://github.com/nighthawkcoders/devOps.git devops

cd devops
```

- Install python dependencies for Flask, etc.

```bash
pip install -r requirements.txt
```

- Run from Terminal without VSCode

    - Run python from command line and check server
    ```bash
    python main.py
    ```

- Prepare VSCode and run
    
    - From Terminal run VSCode
    ```bash
    code .
    ```


### Idea
> The purpose of project is to serve APIs for managing Student and Classroom data.  It is the backend piece of a Full-Stack project.  There may be many frontend companions to the project, based off of year and curriculum.

### Incubator Project, see [Terraform Automation Plan](https://nighthawkcoders.github.io/teacher//c7.0/c7.1/c7.2/2024/01/04/terraform-autmation_IPYNB_2_.html)
> Building Student Desktop workspaces in the cloud
- Infrastructure: AWS, Kasm Workspaces 
- Tooling: Python, Terraform, AWS CLI, Python BOTO module, Kasm Developer API
- SQL Database: User Database and APIs
