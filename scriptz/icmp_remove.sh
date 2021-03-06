#!/bin/bash

for i in `aws ec2 describe-security-groups --query 'SecurityGroups[*].{ID:GroupId}' --output text` 
do
	aws ec2 revoke-security-group-ingress --group-id $i --ip-permissions '[{"IpProtocol": "icmp", "FromPort": 8, "ToPort": -1, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]'
done
