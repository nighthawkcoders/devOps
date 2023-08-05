## Terraform Usage/Test

#### 1st Stage - EC2 Instances Only:
Create a folder for your test (e.g., stage1).
- Place your variable.tf, ec2_install.sh.tpl, and main.tf files in the folder.
- Run `terraform init` to initialize the project.
- Run `terraform plan` to see what resources will be created.
- If the plan looks good, run `terraform apply to create the EC2 instances.
- Manually check the AWS Management Console to ensure that the EC2 instances are created with the correct tags and elastice IPs.
- Terraform provides the `terraform destroy` command, which you can use to destroy all the resources created by a specific Terraform configuration. Run this before moving on to next test.
- Check that created EC2's and Elastic IPs are gone.

#### 2nd Stage - EC2 Instances and Route 53 Records:
Create a new folder for this test (e.g., stage2)
- Add network.tf to previous files set.
- Run `terraform init` in this folder.
- Run `terraform plan` to see what resources will be created.
- If the plan looks good, run terraform apply to create the Route 53 records.
- Manually check the AWS Management Console to ensure that the Route 53 records are created correctly.
- Run `terraform destroy`
- Check that created EC2's and Elastic IPs are gone.

#### 3rd Stage - EC2 Instances, Route 53 Records, and Nginx Configurations:
Run final test from version control folder.
- Run `terraform init` in this folder.
- Run `terraform plan` to see what resources will be created.
- If the plan looks good, run `terraform apply` to create the Nginx configurations.
- Manually check the AWS Management Console to ensure that the Nginx configurations are created in correct location.
- Test access of each EC2 instance from internet (eg. kasm2.nighthawkcodingsociety.com)
- Test access to Kasm workspaces by logging in.
- Leave these running and start testing Kasm registry and workspaces if all is well.

## Terraform Architecture
This breakdown shows the hierarchical relationship between the variables, main module and its sub-modules. The main module calls the EC2, Kasm, Networking, Security, etc. to set up key portions of system.

Terraform Module Breakdown for EC2 Instances and Kasm Workspaces

```

File Provisioner (ec2_install.sh.tmp)
|---> Install script for EC2

Variable (variable.tf)
|---> Centralizes unique configuration settings.


Main (Root Module)
|---> Creates AWS EC2 Instances
|---> Configures inbound traffic, sets up elastic ips
|---> Installs Kasm and network tools on EC2

#2. Network.tf
|---> Sets Up DNS in Route 53

#3. Nginx
|---> Configure nginx template through file provision
|---> Moves nginx.conf file into appropriate system location
|---> Depends on main.tf and network.tf

#4. Future, Security and Workspace setups
|---> Defines Kasm roles, Policies, and Security Groups
|---> Input Variables: permissions, security_groups, etc.
|---> Round-robin user population across instances (Terraform?)

#5. Reboot
|---> Checks that other resources have been created
|---> Performs reboot so that all services are activated
|---> Depends on nginx.tf

```