import boto3
import schedule
import logging
import paramiko
import os
from botocore.exceptions import ClientError

ssh = paramiko.SSHClient()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ec2_status.log"),
        logging.StreamHandler()
    ]
)

# Fetch AWS region from environment variables or fallback to a default value
AWS_REGION = os.getenv('AWS_REGION', 'eu-central-1')

# Initialize EC2 client and resource
ec2_client = boto3.client('ec2', region_name=AWS_REGION)
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)

instance_ids = []

def get_public_ip(instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instances = response['Reservations'][0]['Instances']

    # Extract the public IP
    for instance in instances:
        public_ip = instance.get('PublicIpAddress')
        if public_ip:
            instance_ids.append(instance['InstanceId'])
            return public_ip
        else:
            return "No public IP assigned"

def check_instance_status():
    try:
        # Describe instance statuses, including all instances
        statuses = ec2_client.describe_instance_status(IncludeAllInstances=True)

        # Loop through each instance status and log the information
        for status in statuses['InstanceStatuses']:
            ins_status = status['InstanceStatus']['Status']
            sys_status = status['SystemStatus']['Status']
            state = status['InstanceState']['Name']
            instance_id = status['InstanceId']
            logging.info(f"Instance {instance_id} is {state} with instance status {ins_status} and system status {sys_status}")
            public_ip = get_public_ip(instance_id)

            # connect using ssh
            ssh.connect(public_ip, 22, 'root')

    except ClientError as e:
        logging.error(f"Error fetching EC2 instance status: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

## add tags to all EC2 instances
response = ec2_resource.create_tags(
    Resources=instance_ids,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'Dev'
        },
    ]
)

# Schedule the check to run every 10 seconds
schedule.every(10).seconds.do(check_instance_status)

