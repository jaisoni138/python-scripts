import boto3

def list_running_instances(region):
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A')
            })
    
    return instances

def terminate_instance(region, instance_id):
    ec2_client = boto3.client('ec2', region_name=region)
    ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(f"EC2 Instance {instance_id} terminated successfully.")

# Example usage:
region = 'us-west-2'
running_instances = list_running_instances(region)
print("Running EC2 instances:", running_instances)

# Terminate an instance by ID (ensure this is a valid instance ID)
# terminate_instance(region, 'i-0abcd1234efgh5678')
