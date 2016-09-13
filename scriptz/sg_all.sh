#!/bin/bash

sg=$1
port=$2

aws ec2 authorize-security-group-ingress --group-id $sg --protocol tcp --port $port --cidr 0.0.0.0/0
