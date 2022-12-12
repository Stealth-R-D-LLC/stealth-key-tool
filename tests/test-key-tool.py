#! /usr/bin/env python

import os
import string
import getpass

import stealth_key_tool as skt

def test():

  mnemonic = 'aware report movie exile buyer drum poverty supreme gym oppose float elegant'
  key = skt.key_from_mnemonic(mnemonic)

  print("--------------------------------------------------------")

  # XST
  print("Expected XST Address: Ry9h2KZqgMMtNBZ33ukKVNrFFK3w7BLGys")
  child_xst = skt.get_child_key(key, skt.PURPOSE, skt.COIN_XST, 0, 0, 0)
  address_xst = skt.get_address(child_xst, skt.NET_XST)
  assert (address_xst == "Ry9h2KZqgMMtNBZ33ukKVNrFFK3w7BLGys")
  print("XST address is:       %s" % address_xst)

  # BTC
  print("Expected BTC Address: 1A9vZ4oPLb29szfRWVFe1VoEe7a2qEMjvJ")
  child_btc = skt.get_child_key(key, skt.PURPOSE, skt.COIN_BTC, 0, 0, 0)
  address_btc = skt.get_address(child_btc, skt.NET_BTC)
  assert (address_btc == "1A9vZ4oPLb29szfRWVFe1VoEe7a2qEMjvJ")
  print("BTC address is:       %s" % address_btc)

  print("--------------------------------------------------------")
  print("All tests passed")
  print("--------------------------------------------------------")

if __name__ == "__main__":
    test()
