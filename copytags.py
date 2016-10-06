#!/usr/bin/python
import boto3
import sys

ec2 = boto3.resource('ec2')

source = sys.argv[1]
target = sys.argv[2]

if 'i-' not in source:
    source = 'i-' + source
if 'i-' not in target:
    target = 'i-' + target

source_instance = ec2.Instance(source)
target_instance = ec2.Instance(target)


if source_instance.tags is not None:
    try:
        for tag in source_instance.tags:
            if tag['Key'] != 'Name' and tag['Key'] != 'Customer Name':
                print ('Copying Tag Value {} to Key {}.'.format(tag['Value'], tag['Key']))
                target_instance.create_tags(
                    DryRun=False,
                    Tags=[
                        {
                            'Key': tag['Key'],
                            'Value': tag['Value']
                        }
                    ]
                )
    except Exception, e:
        print ('Error message: {}'.format(e))
