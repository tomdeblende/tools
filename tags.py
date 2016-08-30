#!/usr/bin/python
import boto3
import time

ec2 = boto3.resource('ec2')

volumes = ec2.volumes.all()

total = 0


for v in volumes: 
  for x in range(5):
    try:
      iid = v.attachments[0]['InstanceId']
      i = ec2.Instance(iid)
      itn = [tag['Value'] for tag in i.tags if tag['Key'] == 'Name'][0]
      vd = v.attachments[0]['Device'].replace("/dev/", "-")
      tn = itn + vd
      print "Setting Name Tag of " + str(v) + " on " + itn + " to " + tn
      t = v.create_tags(
        DryRun=False,
        Tags=[
          {
            'Key': 'Name',
            'Value': tn
          }
        ]
      )
    except:
      print "Failed to set tags, retrying in 5 seconds"
      time.sleep(5)
    else:
      break
