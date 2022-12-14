#! /usr/bin/env bash
CR=$'\n'  # new line must end every command
ACCOUNT=4
INPUT="sa ${ACCOUNT} ${CR}"  # set account
INPUT+="int ${CR}"           # make change addresses
for i in {0..3}
do
  INPUT+="si ${i} ${CR}"     # set the address index
  INPUT+="addr ${CR}"        # output the address
done
stealth-key-tool.py -S <<< "${INPUT}"
