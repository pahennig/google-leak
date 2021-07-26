#!/bin/bash
SHELL=/bin/bash
PWD=/root
PATH=/sbin:/bin:/usr/sbin:/usr/bin

# Ensure to change this variable according to the path where your base file is stored
mydir=/home/ec2-user/blue-team/google-leak/

docker run \
    -h google-leak \
	-v $mydir:/usr/app \
	prh/google-leak unicorns 192.168.100.30 514
    