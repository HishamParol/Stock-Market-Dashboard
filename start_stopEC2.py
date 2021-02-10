import boto3
import json

region = "eu-west-2"

instances = 'ENTER YOUR INSTANCE ID'

ec2 = boto3.client("ec2", region_name=region)

def checking():
    response = ec2.describe_instance_status(InstanceIds=[instances])
    if len(response["InstanceStatuses"])==0:
        print(response)
        checking()
    return

def lambda_handler(event, context):
    
    button=int(event['key1'])
    if button==1:
        ec2.start_instances(InstanceIds=[instances])
        checking()
        status="starting your instances: " + str(instances)
        #call some delay function
    elif button==2:
        ec2.stop_instances(InstanceIds=[instances])
        status="stopped your instances: " + str(instances)
	
   
    return status
