#!/bin/bash

sg=$1
port=$2

aws ec2 authorize-security-group-ingress --group-id $sg --protocol udp --port $port --cidr 172.25.152.0/22
aws ec2 authorize-security-group-ingress --group-id $sg --protocol udp --port $port --source-group sg-76feb612
aws ec2 authorize-security-group-ingress --group-id $sg --protocol udp --port $port --source-group sg-f687c592
aws ec2 authorize-security-group-ingress --group-id $sg --protocol udp --port $port --source-group sg-dd7634b9
aws ec2 authorize-security-group-ingress --group-id $sg --protocol udp --port $port --source-group sg-907634f4
aws ec2 authorize-security-group-ingress --group-id $sg --protocol udp --port $port --source-group sg-1287c576
