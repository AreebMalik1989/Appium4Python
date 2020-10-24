#!/bin/bash
# Used to obtain the verification code for mobile phone login, here is just an example, the relevant address have been hidden.

# Phone number
MOBILE=$1

# Token
TOKEN="xxxxxxxxxxxxxxxxxxxxxx"

CODE=`curl -s "http://xxxxxx?token=$TOKEN&mobile=$MOBILE" | awk -F ',' '{print $9;}' | awk -F ':' '{print $3;}' | awk -F '}' '{print $1;}'`

echo $CODE
