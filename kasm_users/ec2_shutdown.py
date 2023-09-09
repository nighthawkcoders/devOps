import boto3
from datetime import datetime, time
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

# AWS credentials
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

# Get all available regions
ec2 = boto3.client(
    "ec2",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-west-2'  # Use any region to list all regions
)

all_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Connect to EC2 in each region
def connect_to_ec2(region):
    return boto3.client(
        "ec2",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=region
    )

def get_instances_to_manage(ec2_client):
    response = ec2_client.describe_instances(
        Filters=[{"Name": "tag:Name", "Values": ["Kasm*"]}]
    )

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance["InstanceId"])

    return instances

def stop_instances(ec2_client, instance_ids):
    if instance_ids:
        ec2_client.stop_instances(InstanceIds=instance_ids)
        print(f"Stopped instances: {instance_ids}")
    else:
        print("No instances to stop.")

def start_instances(ec2_client, instance_ids):
    if instance_ids:
        ec2_client.start_instances(InstanceIds=instance_ids)
        print(f"Started instances: {instance_ids}")
    else:
        print("No instances to start.")

def main():
    current_time = datetime.now().time()
    shutdown_time = time(0, 0)  # 12:00 AM
    startup_time = time(6, 0)   # 06:00 AM

    for region in all_regions:
        ec2_client = connect_to_ec2(region)
        instances_to_manage = get_instances_to_manage(ec2_client)

        if shutdown_time <= current_time < startup_time:
            stop_instances(ec2_client, instances_to_manage)
        elif startup_time <= current_time:
            start_instances(ec2_client, instances_to_manage)

if __name__ == "__main__":
    main()
