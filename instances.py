#!/usr/bin/python
import boto3

ec2 = boto3.resource('ec2')

instances = ec2.instances.all()

print "instance-id,instance name,application,environment"

for i in instances:
    inn = [tag['Value'] for tag in i.tags if tag['Key'] == 'Name'][0]
    ine = [tag['Value'] for tag in i.tags if tag['Key'] == 'environment'][0]
    ina = [tag['Value'] for tag in i.tags if tag['Key'] == 'application'][0]
    print i.id + "," + inn + "," + ina + "," + ine

