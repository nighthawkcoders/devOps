## Developer Operations for Nighthawk Students and Infrastructure
[WIP Admin Server]9https://devops.nighthawkcodingsociety.com/0
[Terraform Automation Plan](https://nighthawkcoders.github.io/teacher//devops/cloud_workspace)

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

### History of Project, see [Terraform Automation Plan](https://nighthawkcoders.github.io/teacher//devops/cloud_workspace)
> Building Student Desktop workspaces in the cloud
- Infrastructure: AWS, Kasm Workspaces 
- Tooling: Python, Terraform, AWS CLI, Python BOTO module, Kasm Developer API
- SQL Database: User Database and APIs

### Database Migration
> In case of Schema change it is important to upgrade database as follows.  

- Install flask app
```bash
export FLASK_APP=main
export PYTHONPATH=.:$PYTHONPATH  # flask need . to find files
flask db init
flask db upgrade
```

- It may be easiest to have a Docker file to do this on production environment.  We should backup database before schema upgrade

```bash
ENV FLASK_APP=main
ENV PYTHONPATH=.:$PYTHONPATH
RUN flask db init
RUN flask db upgrade
```

# Scripts
## Creating AWS Users
- GET /create_users, it will create AWS users from the GH ids in database if they don't exist
## Updating KASM servers in datbaase
- GET /update_users_kasm, it will find the KASM server for each user in the database and update their DB Entry
## Migrating Database
- ./migrate.sh
