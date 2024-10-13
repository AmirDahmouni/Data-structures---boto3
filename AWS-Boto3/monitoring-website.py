import boto3
import paramiko
import time
import os
import smtplib
from email.mime.text import MIMEText

# Set environment variables for email credentials and AWS instance details
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# AWS Configuration
EC2_INSTANCE_ID = "i-48181ef-615"
REGION_NAME = "eu-west-2"
KEY_FILE_PATH = "path/to/my/private-key.pem"
SSH_USER = "ec2-user"

# Initialize boto3 EC2 client
ec2_client = boto3.client('ec2', region_name=REGION_NAME)


def send_notification(message):
    """ Sends email notifications if the application goes down. """
    msg = MIMEText(message)
    msg['Subject'] = 'Application Down'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())


def restart_ec2_instance():
    """ Restart the EC2 instance. """
    ec2_client.reboot_instances(InstanceIds=[EC2_INSTANCE_ID])
    print(f"Rebooting EC2 instance: {EC2_INSTANCE_ID}")

    # Wait for the instance to be back in 'running' state
    while True:
        response = ec2_client.describe_instance_status(InstanceIds=[EC2_INSTANCE_ID])
        if response['InstanceStatuses'] and response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
            print(f"EC2 instance {EC2_INSTANCE_ID} is running.")
            break
        time.sleep(10)


def restart_docker_container():
    """ Restart the Docker container on the EC2 instance via SSH. """
    try:
        # Establish SSH connection to EC2 instance
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=get_instance_public_ip(), username=SSH_USER, key_filename=KEY_FILE_PATH)

        # Restart Docker container
        command = "docker restart my-app"  # Replace with your container ID or name
        stdin, stdout, stderr = ssh.exec_command(command)
        print(f"Restarting Docker container: {stdout.read().decode()}")

        ssh.close()
    except Exception as e:
        print(f"Failed to restart Docker container: {e}")


def get_instance_public_ip():
    """ Retrieve the public IP address of the EC2 instance. """
    response = ec2_client.describe_instances(InstanceIds=[EC2_INSTANCE_ID])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']


def check_application_status():
    app_is_down = True
    return app_is_down



if check_application_status():
    # If the application is down, restart the EC2 instance and container
    print("Application is down. Rebooting EC2 instance and restarting Docker container.")
    send_notification("Application is down. Rebooting EC2 instance.")

    restart_ec2_instance()  # Reboot EC2 instance
    restart_docker_container()  # Restart Docker container

