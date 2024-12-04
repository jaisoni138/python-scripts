import boto3

def get_unattached_volumes(region='us-east-1'):
    ec2_client = boto3.client('ec2', region_name=region)
    
    # Describe all volumes
    response = ec2_client.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    
    unattached_volumes = response['Volumes']
    
    return unattached_volumes

def delete_volume(volume_id, region='us-east-1'):
    ec2_client = boto3.client('ec2', region_name=region)
    
    try:
        ec2_client.delete_volume(VolumeId=volume_id)
        print(f"Volume {volume_id} deleted successfully.")
    except Exception as e:
        print(f"Failed to delete volume {volume_id}: {e}")

def main(region='us-east-1'):
    unattached_volumes = get_unattached_volumes(region)
    
    if not unattached_volumes:
        print("No unattached volumes found.")
        return
    
    for volume in unattached_volumes:
        volume_id = volume['VolumeId']
        print(f"Found unattached volume: {volume_id}")
        delete_volume(volume_id, region)

if __name__ == "__main__":
    main()
