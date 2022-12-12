#! /usr/bin/env bash
DONT_USE_THIS_MNEMONIC="some random words"
ACCOUNT=4
INPUT=${DONT_USE_THIS_MNEMONIC}$'\nsa '${ACCOUNT}$'\nint'
for i in {0..3}
do
  INPUT=${INPUT}$'\nsi '${i}$'\naddr'
done
stealth-key-tool.py -N <<< "${INPUT}"
