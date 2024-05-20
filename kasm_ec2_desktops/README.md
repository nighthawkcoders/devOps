## Terraform Usage/Test
### Terraform Test Commands and SDLC:
Go to Kasm version control folder, then run these commands.
- M1 to M3 updates to support Terraform with Apple Silicon
    - brew install kreuzwerker/taps/m1-terraform-provider-helper
    - m1-terraform-provider-helper activate
    - m1-terraform-provider-helper install hashicorp/template -v v2.2.0
    - NOTE: This version of Devops now supports Apple Silicon M1-M3 so some of these commands may not be necessary. Use at your own risk, any issues please contact the original authors J Mortensen, T Patil, and R Jaiswal. All following commands are the same as the original DevOps project.
- Run a `terraform init` to initialize the project.
- Run a `terraform plan` to see what resources will be created.
- If the plan looks good, run `terraform apply` to create the Nginx configurations.
- Perform review and analysis on the AWS Console
- Perform review, test, and analysis by running Kasm server from the Browser.
- Update or commit code changes if you have an incrementally successful run.
- If you are done with testing and review perform `terraform destroy` command.
- Continue with Terraform SDLC: code-init-plan-apply-commit-destroy cycle.

- If the plan looks good, run the `terraform apply` command to create the EC2 instances.

- Terraform provides the Check that the created EC2s and Elastic IPs are gone.

### Terraform Production Commands
Run these commands to build EC2 instances

### Typical Test
Create an instance, perform tests, and then come back quickly and destroy. 

```bash
terraform init
terraform plan -var="instances_start=2"
terraform apply -var="instances_start=2"
# ... test time ...
terraform destroy
```

### Single workspace with Plan
The remaining portion of this is trying to make a plan, apply the plan, and destroy it.

Option A plan - Create 1 instance starting at 5.  

```bash
terraform init
terraform plan -var="instances_start=5" -out=opA.tfplan
terraform apply opA.tfplan
```

Option B - Create 2 instances starting at 10.  This has the behavior of destroying previous elements, for instance starting at 5

```bash
terraform plan -var="instances_start=10" -var="instances_count=2" -out=opB.tfplan
terraform apply opB.tfplan
```

Destroy a portion of saved plan opB.tfplan
```bash
terraform destroy

```

### Two Workspace
The remaining portion of this is trying to make a plan, apply the plan, and destroy it.

DevOps Machines 1 - Create 1 instance starting at 50.  Follow terraform commands, review plan and follow Test and Review below.

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/nighthawkcoders/devOps.git dop1
cd ~/projects/dop1/kasm
terraform init
terraform plan -var="instances_start=50" -out=plan.tfplan
terraform apply plan.tfplan
terraform show
```

DevOps Machines 2 - Create 3 instances starting at 100.   Follow terraform commands, review plan and the following Test and Review below.

```bash
cd ~/projects
git clone https://github.com/nighthawkcoders/devOps.git dop2
cd ~/projects/dop1/kasm
terraform plan -var="instances_start=100" -var="instances_count=3" -out=plan.tfplan
terraform apply plan.tfplan
terraform show
```

Destroy from dop1.  Review the destroy plan and make sure dop2 projects are still available.
```bash
cd ~/projects/dop1
terraform destroy

cd ~/projects/dop1
terraform show
```


### Test and Review 
Test these items to ensure EC2 and Kasm functionality
- In coding and testing be sure to `follow SDLC above`.  Terraform has errors that can occur in init, plan, and apply.  I think of init as typos/syntax, plan as logic checking, and apply as deployment/runtime checking.  ChatGPT is a great resource for all Terraform error messages.
- Be sure to review the `terraform plan` output.  Check all the data to see if it makes sense before running the `terraform apply` command.  Check that the correct number of resources are generated and that the assignments of data look correct.  Most of my logic errors in Terraform coding are found by reviewing the plan. 
- Check the AWS Management Console for `EC2/EC2 Dashboard/Instances`; validate the `Tags`, `Elastic IPs`, and `Security Groups`.  This is a place where I have found errors in my Terraform coding logic; like a resource being duplicated.
`Use the Console` to Connect to a specific EC2 Instance ID.  I use the vi or vim editor and search the log /var/log/cloud-init-output.log.  Many echo messages have been intentionally made in ec2_install.sh.tpl, called scaffolding, to lock for in the editor.  Through multiple terraform apply commands and scaffolding anyone can work through shell errors.  
- `Kasm Testing`, log in through the browser to admin and user accounts.  You can find passwords by looking for admin@kasm.local in /var/logcloud-init-output.log or --admin-password and --user-password in ec2_install.sh.tpl in test automation.  Start testing `Kasm registry and workspaces`

#### 3rd Stage - EC2 Instances, Route 53 Records, and Nginx Configurations:
- Run the `terraform init` in this folder.
- Run the `terraform plan` to see what resources will be created.
- Manually check the AWS Management Console to ensure that the Nginx configurations are created in the correct location.
- Test access of each EC2 instance from internet (eg. kasm2.nighthawkcodingsociety.com)
- Test access to Kasm workspaces by logging in.
- Leave these running and start testing Kasm registry and workspaces if all is well.

## Terraform Architecture
This breakdown shows the hierarchical relationship between files (mostly .tf modules) and functions.

Terraform Module Breakdown

```

EC2 install script (.sh.tmp)
|---> Downloads and installs Kasm
|---> Sets up and configures nginx and certbot
|---> Uses Terraform file provisioning for custom EC2 requirements

Variable (variable.tf)
|---> Centralizes unique variables.
|---> Sets EC2 instance names and quantity
|---> Sets email, route 53 hosted zone, or other future external depenencies

AWS Instances (ec2.tf)
|---> Creates AWS EC2's
|---> Install Ubuntu AMI
|---> Sets key pair
|---> Sets security group
|---> Launches install script through user_data

Network.tf
|---> Sets Up public facing Elastice IP's
|---> Maps Elastic IP to EC2
|---> Sets Up DNS A records, Domain names to public IP's

Security (security.tf)
|---> Configures inbound traffic: SSH, HTTP, HTTPS
|---> Allows all outbound traffic

TBD, Kasm Configuration (not started)
|---> Defines Kasm roles, Policies, and Security Groups
|---> Input Variables: permissions, security_groups, etc.
|---> Round-robin user population across instances (Terraform?)

TBD, Reboot (reboot.tf.exclude)
|---> Still investigating approaches
|---> Sleeps for 15 minutes and then reboot all EC2's created
|---> Performs reboot to verify all services reactivate

```

## Other documentation

Variable Names: Make some of them even more specific, like kasm_instance_prefix instead of instance_name, or starting_instance_number could become instance_number_start.

Resource Names: Remove Kasm from resources.  Make a system so it could be used for another application, let data and shell script where deltas happen.

Error Handling: Review shell script for basic error handling and logging improvements.
