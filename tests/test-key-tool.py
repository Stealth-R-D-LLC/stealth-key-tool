#! /usr/bin/env python

import os
import string
import getpass

import stealth_key_tool as skt

def test():

  mnemonic = 'aware report movie exile buyer drum poverty supreme gym oppose float elegant'
  key = skt.key_from_mnemonic(mnemonic)

  print("----------------------------------------------------------------")

  # XST
  print("Expected XST Address: Ry9h2KZqgMMtNBZ33ukKVNrFFK3w7BLGys")
  child_xst = skt.get_child_key(key, skt.PURPOSE, skt.XST.coin, 0, 0, 0)
  address_xst = skt.get_p2pkh_address(child_xst, skt.XST.addr_net_byte)
  assert (address_xst == "Ry9h2KZqgMMtNBZ33ukKVNrFFK3w7BLGys")
  print("XST address is:       %s" % address_xst)

  # BTC
  print("Expected BTC Address: 1A9vZ4oPLb29szfRWVFe1VoEe7a2qEMjvJ")
  child_btc = skt.get_child_key(key, skt.PURPOSE, skt.BTC.coin, 0, 0, 0)
  address_btc = skt.get_p2pkh_address(child_btc, skt.BTC.addr_net_byte)
  assert (address_btc == "1A9vZ4oPLb29szfRWVFe1VoEe7a2qEMjvJ")
  print("BTC address is:       %s" % address_btc)

  # ETH
  print("Expected ETH Address: 0xC5e19e780D06cBE23d4D972806bc5D30C9f3EFA3")
  child_eth = skt.get_child_key(key, skt.PURPOSE, skt.ETH.coin, 0, 0, 0)
  address_eth = skt.get_eth_address(child_eth, skt.ETH.addr_net_byte)
  assert (address_eth  == "0xC5e19e780D06cBE23d4D972806bc5D30C9f3EFA3")
  print("ETH address is:       %s" % address_eth)

  print("----------------------------------------------------------------")
  print("All tests passed")
  print("----------------------------------------------------------------")

if __name__ == "__main__":
    test()
