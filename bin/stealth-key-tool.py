#! /usr/bin/env python

# Copyright (c) 2022, James Stroud
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys
import string
import getpass
import argparse

from stealth_key_tool import *

ABET = string.ascii_lowercase + string.whitespace

def setup_args():
  parser = argparse.ArgumentParser(description="HD Wallet Key Tool")
  parser.add_argument('--non-interactive', '-N', dest="interactive",
                      default=True, action='store_false',
                      help="use non-interactively")
  return parser.parse_args()

def pstderr(*args):
  print(*args, file=sys.stderr)

def print_path(account, change, index, interactive=True):
  if interactive:
      pstderr(get_path(account, change, index))

def get_input(prompt=None, interactive=True):
  if prompt and interactive:
      sys.stderr.write(str(prompt))
  return input()

def print_help():
  pstderr("---------------------------------------")
  pstderr("                  HELP")
  pstderr("---------------------------------------")
  pstderr("     h  - help")
  pstderr("  addr  - get address")
  pstderr("    gp  - get path")
  pstderr("    sa  - set account")
  pstderr("   ++a  - increment account")
  pstderr("   --a  - decrement account")
  pstderr("   ext  - set external (not change)")
  pstderr("   int  - set internal (change)")
  pstderr("    si  - set address index")
  pstderr("   ++i  - increment address index")
  pstderr("   --i  - increment address index")
  pstderr("    sp  - set path")
  pstderr("  xpub  - account extended public key")
  pstderr("  xprv  - account extended private key")
  pstderr("   pub  - hex public key")
  pstderr("   prv  - hex private key")
  pstderr("   wif  - wallet import format")
  pstderr("     q  - quit")
  pstderr("---------------------------------------")

def get_mnemonic(interactive):
  if (interactive):
    m = getpass.getpass("Secret phrase (hit enter for visible input): ")
  else:
    m = ""
  if (m == ""):
    m = get_input("Secret phrase:\n", interactive)
  m = "".join([v.lower() for v in m if v.lower() in ABET])
  return " ".join(m.split())

def main_loop(args):
  interactive = args.interactive
  mnemonic = get_mnemonic(interactive)
  key = key_from_mnemonic(mnemonic)

  account = 0
  change = 0
  index = 0
  while True:
    b = get_input("Command: ", args.interactive)
    b = b.strip().split(maxsplit=1)
    if len(b) == 0:
      c = "h"
      p = None
    elif len(b) == 1:
      c = b[0]
      p = None
    else:
      c, p = b

    ###  quit  ###
    if c == "q":
      break
    ###  help  ###
    elif c.lower() in ["h", "?", "help"]:
      print_help()
    ###  set account  ###
    elif c == "sa":
      if (p is None):
        p = get_input("Enter account identifier:")
      try:
        acc = parse_account_id(p)
      except Exception as e:
        pstderr(e)
        continue
      account = acc
      print_path(account, change, index, interactive)
    ###  increment account  ###
    elif c == "++a":
      account += 1
      print_path(account, change, index, interactive)
    ###  decrement account  ###
    elif c == "--a":
      if account < 1:
        pstderr("Account can't be decremented")
      else:
        account -= 1
        print_path(account, change, index, interactive)
    ###  set external  ###
    elif c == "ext":
      change = 0
      print_path(account, change, index, interactive)
    ###  set internal  ###
    elif c == "int":
      change = 1
      print_path(account, change, index, interactive)
    ###  set address index  ###
    elif c == "si":
      if p is None:
        p = get_input("Enter address index:")
      try:
        idx = parse_address_index(p)
      except Exception as e:
        pstderr(e)
        continue
      index = idx
      print_path(account, change, index, interactive)
    ###  increment address index  ###
    elif c == "++i":
      index += 1
      print_path(account, change, index, interactive)
    ###  decrement address index  ###
    elif c == "--i":
      if index < 1:
        pstderr("Address index can't be decremented")
      else:
        index -= 1
        print_path(account, change, index, interactive)
    ###  get public key  ###
    elif c == "pub":
      child = get_child_key(key, PURPOSE, COIN_XST, account, change, index)
      print(child.PublicKey().hex())
    ###  get private key ###
    elif c == "prv":
      child = get_child_key(key, PURPOSE, COIN_XST, account, change, index)
      print(child.PrivateKey().hex())
    ###  get wallet import format  ###
    elif c == "wif":
      child = get_child_key(key, PURPOSE, COIN_XST, account, change, index)
      print(get_wif(child))
    ###  set path  ###
    elif c == "sp":
      if p is None:
        p = get_input("Enter path (account/change/index): ")
      try:
        account, change, index = parse_path(p)
      except Exception as e:
        pstderr(e)
        continue
      print_path(account, change, index, interactive)
    ###  get path  ###
    elif c == "gp":
      print(get_path(account, change, index))
    ###  get address  ###
    elif c == "addr":
      child = get_child_key(key, PURPOSE, COIN_XST, account, change, index)
      address = get_address(child, NET_XST)
      print(address)
    ###  get extended public key  ###
    elif c == "xpub":
      child = get_child_key(key, PURPOSE, COIN_XST, account)
      print(child.ExtendedKey(private=False))
    ###  get extended private key  ###
    elif c == "xprv":
      child = get_child_key(key, PURPOSE, COIN_XST, account)
      print(child.ExtendedKey(private=True))
    ###  command not recognized  ###
    else:
      pstderr("Command \"%s\" not recognized" % c)

def main():
  args = setup_args()
  try:
    main_loop(args)
  except (KeyboardInterrupt, EOFError):
    if args.interactive:
      pstderr()
  if args.interactive:
    pstderr("Quitting")


if __name__ == "__main__":
  main()