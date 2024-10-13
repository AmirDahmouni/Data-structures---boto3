import boto3
from operator import itemgetter

# Create an EC2 client to interact with EC2 resources in the specified region
ec2_client = boto3.client('ec2', region_name="eu-west-3")

# Retrieve information about volumes that have the tag 'environment' set to 'Dev'
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'tag:environment',  # Filtering by tag 'environment'
            'Values': ['Dev']
        }
    ]
)

# Iterate through the list of volumes retrieved
for volume in volumes['Volumes']:
    # For each volume, retrieve the associated snapshots
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],  # Only look for snapshots owned by the current AWS account
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )

    # Sort the snapshots by the 'StartTime' field in descending order (newest to oldest)
    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    # Keep the two most recent snapshots and delete the rest
    for snap in sorted_by_date[2:]:  # [2:] skips the first two snapshots (most recent)
        # Delete the older snapshots, keeping the two most recent
        response = ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )

        print(response)
