#!/usr/bin/python
import boto3

ec2 = boto3.resource('ec2')

volumes = ec2.volumes.all()

total = 0

print "Volume,Size,Type,State"

for v in volumes: 
    if 'Name' in str(v.tags):
        vn = [tag['Value'] for tag in v.tags if tag['Key'] == 'Name'][0]
        print vn + "," + str(v.size) + "," + v.volume_type
        total = total + v.size
print "Total:" + "," + str(total)
