#! /usr/bin/env bash
DONT_USE_THIS_MNEMONIC="some random wordsx"
ACCOUNT=4
for i in {0..3}
do
stealth-key-tool.py -N << EOF
${DONT_USE_THIS_MNEMONIC}
sa $ACCOUNT
int
si ${i}
addr
EOF
done
