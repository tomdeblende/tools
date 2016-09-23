#!/bin/bash

for i in `aws ec2 describe-security-groups --query 'SecurityGroups[*].{ID:GroupId}' --output text` 
do
	aws ec2 authorize-security-group-ingress --group-id $i --protocol tcp --port 22 --source-group sg-dc0655b8
done
