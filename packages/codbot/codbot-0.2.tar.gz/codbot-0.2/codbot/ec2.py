import boto3
import json

ec2 = boto3.resource('ec2')

#parse ec2.json file for EC2 specs
with open('ec2.json', 'r') as f:
    ec2_dict = json.load(f)

#read each element
for v in ec2_dict['ec2']:

#create a new EC2 instance
  instances = ec2.create_instances(
    ImageId=v['ImageId'],
    InstanceType=v['InstanceType'],
    KeyName=v['KeyName'],
    MinCount=v['MinCount'],
    MaxCount=v['MaxCount']
 )
