import boto3
from datetime import datetime, timedelta

# Initialize boto3 client
cloudwatch = boto3.client('cloudwatch')
autoscaling = boto3.client('autoscaling')

def get_cpu_utilization(instance_id):
    # Get the average CPU utilization for the last 5 minutes
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)

    response = cloudwatch.get_metric_statistics(
        Period=300,  # 5-minute interval
        StartTime=start_time,
        EndTime=end_time,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}]
    )
    
    if len(response['Datapoints']) > 0:
        return response['Datapoints'][0]['Average']
    return None

def scale_auto_scaling_group(group_name, desired_capacity):
    # Update the desired capacity of the Auto Scaling group
    autoscaling.set_desired_capacity(
        AutoScalingGroupName=group_name,
        DesiredCapacity=desired_capacity
    )
    print(f"Scaling {group_name} to {desired_capacity} instances.")

def check_and_scale(group_name, threshold=70.0):
    # Get the list of instances in the Auto Scaling group
    response = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])
    instance_ids = [instance['InstanceId'] for instance in response['AutoScalingGroups'][0]['Instances']]

    # Check CPU utilization for each instance
    for instance_id in instance_ids:
        cpu_utilization = get_cpu_utilization(instance_id)
        
        if cpu_utilization is not None and cpu_utilization > threshold:
            print(f"CPU utilization for instance {instance_id} is {cpu_utilization}%, scaling up.")
            scale_auto_scaling_group(group_name, desired_capacity=5)  # Scale to 5 instances (example)
            break  # Exit after scaling up

# Example usage
check_and_scale('your-auto-scaling-group-name')
