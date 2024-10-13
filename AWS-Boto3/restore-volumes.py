import boto3
from operator import itemgetter

# attach volumes to ec2 instances

ec2_client = boto3.client('ec2', region_name="eu-west-3")
ec2_resource = boto3.resource('ec2', region_name="eu-west-3")

# Specify the instance ID
instance_id = "i-03f01be7a778eaf7e"

# Retrieve all volumes attached to the given EC2 instance
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)


instance_volume = volumes['Volumes'][0]

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)

# Sort the snapshots by the StartTime field in descending order and get the latest one
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot['StartTime'])  # Print the timestamp of the latest snapshot for confirmation

# Create a new volume from the latest snapshot in a specific Availability Zone
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],  # Use the latest snapshot ID to create the new volume
    AvailabilityZone="eu-west-3b",  # Specify the availability zone to create the volume in
    TagSpecifications=[  # Add tags to the new volume
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'environment',
                    'Value': 'Dev'
                }
            ]
        }
    ]
)

# Wait for the new volume to become available before attaching it
while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)

    # Check if the volume is in 'available' state (fully created and ready)
    if vol.state == 'available':
        # Attach the new volume to the same instance at the specified device location
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'  # The device path
        )
        break  # Exit the loop once the volume has been attached
