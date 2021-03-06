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
                volumenametag = ''
                volumeapptag = ''
                volumesuptag = ''
                instancenametag = ''
                instanceapptag = ''
                instancesuptag = ''
                if volume.tags is not None:
                    if [tag['Value'] for tag in volume.tags if tag['Key'] == 'Name']:
                        volumenametag = [tag['Value'] for tag in volume.tags if tag['Key'] == 'Name'][0]
                    if [tag['Value'] for tag in volume.tags if tag['Key'] == 'application']:
                        volumeapptag = [tag['Value'] for tag in volume.tags if tag['Key'] == 'application'][0]
                    if [tag['Value'] for tag in volume.tags if tag['Key'] == 'support']:
                        volumesuptag = [tag['Value'] for tag in volume.tags if tag['Key'] == 'support'][0]
                if instance.tags is not None:
                    if [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name']:
                        instancenametag = [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'][0]
                    if [tag['Value'] for tag in instance.tags if tag['Key'] == 'application']:
                        instanceapptag = [tag['Value'] for tag in instance.tags if tag['Key'] == 'application'][0]
                    if [tag['Value'] for tag in instance.tags if tag['Key'] == 'support']:
                        instancesuptag = [tag['Value'] for tag in instance.tags if tag['Key'] == 'support'][0]
                volumedevice = volume.attachments[0]['Device'].replace("/dev/", "")
                nametag = instancenametag + "-" + volumedevice
                apptag = instanceapptag
                suptag = instancesuptag

                if not nametag:
                    print('No Name tag present for {}'.format(instanceid))
                else:
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
                        print('Skipping: Name Tag of {} on {} was already set to {}'.format(volumedevice,
                                                                                            instancenametag,
                                                                                            nametag))

                if not apptag:
                    print('No Application tag present for {}'.format(instancenametag))
                else:
                    if volumeapptag != apptag:
                        print('Setting Application Tag of {} on {} to {}'.format(volumedevice, instancenametag, apptag))
                        tag = volume.create_tags(
                            DryRun=False,
                            Tags=[
                                {
                                    'Key': 'application',
                                    'Value': apptag
                                }
                            ]
                        )
                    else:
                        print('Skipping: Application Tag of {} on {} was already set to {}'.format(volumedevice,
                                                                                                   instancenametag,
                                                                                                   apptag))

                if not suptag:
                    print('No Support tag present for {}'.format(instancenametag))
                else:
                    if volumesuptag != suptag:
                        print('Setting Support Tag of {} on {} to {}'.format(volumedevice, instancenametag, suptag))
                        tag = volume.create_tags(
                            DryRun=False,
                            Tags=[
                                {
                                    'Key': 'support',
                                    'Value': suptag
                                }
                            ]
                        )
                    else:
                        print('Skipping: Support Tag of {} on {} was already set to {}'.format(volumedevice,
                                                                                               instancenametag, suptag))

            except Exception, e:
                print ('Error message: {}'.format(e))
                print ('Failed to set tags on {}, retrying in 5 seconds'.format(volume))
                time.sleep(5)
            else:
                break
