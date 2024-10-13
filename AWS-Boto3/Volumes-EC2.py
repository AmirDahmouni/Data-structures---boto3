#Volume snapshot (image) of EC2 instance

import boto3
import schedule

ec2_client = boto3.client('ec2', region_name="eu-west-3")

def create_volume_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'environment',
                'Values': ['Dev']
            }
        ]
    )
    for volume in volumes['Volumes']:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId']
        )
        print(new_snapshot)


schedule.every(14).day.do(create_volume_snapshots)

while True:
    schedule.run_pending()





