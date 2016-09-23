#!/usr/bin/python
import boto3
import time

ec2 = boto3.resource('ec2')
volumes = ec2.volumes.all()

for volume in volumes:
    if volume.state == 'in-use':
        for x in range(5):
            try:
                instanceid = volume.attachments[0]['InstanceId']
                instance = ec2.Instance(instanceid)
                if volume.tags is not None:
                    volumenametag = [tag['Value'] for tag in volume.tags if tag['Key'] == 'Name'][0]
                else:
                    volumenametag = ''
                if instance.tags is not None:
                    instancenametag = [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'][0]
                else:
                    instancenametag = ''
                volumedevice = volume.attachments[0]['Device'].replace("/dev/", "")
                nametag = instancenametag + "-" + volumedevice
                if volumenametag != nametag:
                    print('Setting Name Tag of {} on {} to {}'.format(volumedevice, instancenametag, nametag))
                    tag = volume.create_tags(
                        DryRun=False,
                        Tags=[
                            {
                              'Key': 'Name',
                              'Value': nametag
                            }
                        ]
                    )
                else:
                    print('Skipping: Name Tag of {} on {} was already set to {}'.format(volumedevice, instancenametag, nametag))
            except Exception, e:
                print ('Error message: {}'.format(e))
                print ('Failed to set tags on {}, retrying in 5 seconds'.format(volume))
                time.sleep(5)
            else:
                break
