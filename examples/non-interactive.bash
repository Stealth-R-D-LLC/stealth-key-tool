#! /usr/bin/env bash
CR=$'\n'  # new line must end every command
DONT_USE_THIS_MNEMONIC="some random words"
ACCOUNT=4
INPUT="${DONT_USE_THIS_MNEMONIC} $CR"  # provide mnemonic
INPUT+="sa ${ACCOUNT} ${CR}"          # set account
INPUT+="int ${CR}"                     # make change addresses
for i in {0..3}
do
  INPUT+="si ${i} ${CR}"  # set the address index
  INPUT+="addr ${CR}"     # output the address
done
stealth-key-tool.py -N <<< "${INPUT}"
