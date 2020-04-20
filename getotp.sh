#!/bin/bash
# Get the OTP for mobile number

# mobile number
NUMBER=$1

# token
TOKEN='xxxxxxxxxxxxxxxxxxxxxx'

OTP=`curl -s "http://xxxxxx?token=$TOKEN&mobile=$NUMBER" | awk -F ',' '{print $9;}' | awk -F ':' '{print $3;}' | awk -F '}' '{print $1;}'`

echo $OTP
