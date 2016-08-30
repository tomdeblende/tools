#!/usr/bin/python
import boto3
import time
import sys

ec2 = boto3.resource('ec2')
source_instance = ec2.Instance(str(sys.argv[1]))
target_instance = ec2.Instance(str(sys.argv[2]))

if source_instance.tags is not None:
    try:
        for tag in source_instance.tags:
            if tag['Key'] != 'Name':
                target_instance.create_tags(Tags=tag)
    except Exception, e:
        print ('Error message: {}'.format(e))
        time.sleep(5)
