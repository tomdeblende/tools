#!/bin/bash

sg=$1
port=$2

aws ec2 authorize-security-group-ingress --group-id $sg --protocol tcp --port $port --cidr 40.50.0.0/16
aws ec2 authorize-security-group-ingress --group-id $sg --protocol tcp --port $port --cidr 172.25.196.0/23
aws ec2 authorize-security-group-ingress --group-id $sg --protocol tcp --port $port --cidr 172.25.198.0/24
aws ec2 authorize-security-group-ingress --group-id $sg --protocol tcp --port $port --cidr 40.254.0.0/24
aws ec2 authorize-security-group-ingress --group-id $sg --protocol tcp --port $port --source-group sg-2c9ddc48
