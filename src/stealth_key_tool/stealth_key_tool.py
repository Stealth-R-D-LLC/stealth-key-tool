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

import string
import base64
import hashlib

from Crypto.Hash import keccak

from .pbkdf2 import pbkdf2
from .bip32utils import BIP32Key, BIP32_HARDEN, Base58


TEST = False

# see https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki
PURPOSE = 44
# hardened purpose (44')
HPURPOSE = 0x8000002C

# SLIP44 identifiers 
COIN_XST = 125
COIN_TEST = 1
COIN_BTC = 0
COIN_LTC = 2
COIN_DOGE = 3
COIN_ETH = 60
COIN_FTC = 8
COIN_VTC = 28

# net byte values
ADDR_NET_XST = 62
ADDR_NET_BTC = 0
ADDR_NET_LTC = 48
ADDR_NET_DOGE = 30
ADDR_NET_FTC = 14
ADDR_NET_VTC = 71
ADDR_NET_TEST = 111

# wif encoding
WIF_NET_XST = bytes([0xbe])   # 190
WIF_NET_TEST = bytes([0xef])  # 239
WIF_NET_BTC = bytes([0x80])   # 128
WIF_NET_LTC = bytes([0xb0])   # 176
WIF_NET_DOGE = bytes([0x9e])  # 158
WIF_NET_FTC = bytes([0x8e])   # 142
WIF_NET_VTC = bytes([0x80])   # 128
WIF_COMPRESSED = bytes([0x01])  # 1 -> is compressed


class KeyToolError(Exception):
  pass
class CoinError(KeyToolError):
  pass
class AccountError(KeyToolError):
  pass
class ChangeError(KeyToolError):
  pass
class AddressError(KeyToolError):
  pass
class PathError(KeyToolError):
  pass
class NetworkError(KeyToolError):
  pass
class DependencyError(KeyToolError):
  pass

def keccak_256(message):
  k = keccak.new(digest_bits=256)
  k.update(message)
  return k

# generalized for any network byte
def get_p2pkh_address(key, netbyte):
  vh160 = netbyte.to_bytes(1, "big") + key.Identifier()
  return Base58.check_encode(vh160)

# network byte is ignored
def get_eth_address(key, netbyte=None):
  x = keccak_256(key.PublicKey(compressed=False)).hexdigest()[-40:]
  h = keccak_256(x.encode('utf-8')).hexdigest()
  b = []
  for i, c in enumerate(x):
      if c in string.digits:
          b.append(c)
      elif c in "abcdef":
          n = int(h[i], 16)
          if n > 7:
              b.append(c.upper())
          else:
              b.append(c)
  return "0x" + "".join(b)

def get_wif(key, net_byte):
  raw = net_byte + key.k.to_string() + WIF_COMPRESSED
  return Base58.check_encode(raw)

class Currency:
   def __init__(self, name, ticker,
                      coin, addr_net_byte, wif_net_byte,
                      get_addr):
     self.name = name
     self.ticker = ticker
     self.coin = coin 
     self.addr_net_byte = addr_net_byte
     self.wif_net_byte = wif_net_byte
     self._get_address_inner = get_addr
   def get_copy(self):
     return self.__class__(self.name, self.ticker,
                           self.coin,
                           self.addr_net_byte, self.wif_net_byte,
                           self._get_address_inner)
   def get_address(self, child):
     return self._get_address_inner(child, self.addr_net_byte)

XST = Currency("Stealth", "XST",
               COIN_XST, ADDR_NET_XST, WIF_NET_XST,
               get_p2pkh_address)
BTC = Currency("Bitcoin", "BTC",
               COIN_BTC, ADDR_NET_BTC, WIF_NET_BTC,
               get_p2pkh_address)
ETH = Currency("Ethereum", "ETH",
               COIN_ETH, None, WIF_NET_BTC,
               get_eth_address)
LTC = Currency("Litecoin", "LTC",
               COIN_LTC, ADDR_NET_LTC, WIF_NET_LTC,
               get_p2pkh_address)
DOGE = Currency("Dogecoin", "DOGE",
                COIN_DOGE, ADDR_NET_DOGE, WIF_NET_DOGE,
                get_p2pkh_address)
FTC = Currency("Feathercoin", "FTC",
                COIN_FTC, ADDR_NET_FTC, WIF_NET_FTC,
                get_p2pkh_address)
VTC = Currency("Vertcoin", "VTC",
                COIN_VTC, ADDR_NET_VTC, WIF_NET_VTC,
                get_p2pkh_address)


CURRENCIES = { "XST":XST, "BTC":BTC, "ETH":ETH, "LTC":LTC,
               "DOGE":DOGE, "FTC":FTC, "VTC":VTC }

def get_currency(ticker):
  return CURRENCIES[ticker].get_copy()

# included as a reference
def seed_from_mnemonic(mnemonic, salt=""):
  ROUNDS = 2048
  NBYTES = 64
  m = mnemonic.encode("utf-8")
  s = b"mnemonic" + salt.encode("utf-8")
  return  pbkdf2(hashlib.sha512, m, s, ROUNDS, NBYTES)

def key_from_mnemonic(mnemonic, salt=""):
  seed = seed_from_mnemonic(mnemonic, salt)
  return BIP32Key.fromEntropy(seed)

# all practical implementations harden the purpose, coin type, and account
def get_child_key(key, purpose=PURPOSE,
                       coin_type=None,
                       account=None,
                       change=None,
                       address_index=None):
  child1 = key.ChildKey(purpose + BIP32_HARDEN);
  if coin_type is None:
    return child1
  child2 = child1.ChildKey(coin_type + BIP32_HARDEN)
  if coin_type is None:
    return child2
  child3 = child2.ChildKey(account + BIP32_HARDEN)
  if change is None:
    return child3
  child4 = child3.ChildKey(change)
  if address_index is None:
    return child4
  child5 = child4.ChildKey(address_index)
  return child5

def get_path(purpose, coin, account, change, index):
  params = (purpose, coin, account, change, index)
  return "m/%d'/%d'/%d'/%d/%d" % params

def parse_id(p, e):
  try:
    if p[-1] == "'":
      p = p[:-1]
    i = int(p)
    assert (i >= 0)
  except:
    raise e
  return i

def parse_coin_id(p):
  return parse_id(p, CoinError("Coin id \"%s\" not valid" % p))

def parse_account_id(p):
  return parse_id(p, AccountError("Account id \"%s\" not valid" % p))

def parse_address_index(p):
  try:
    idx = int(p)
    assert (idx >= 0)
  except:
    raise AddressError("Address index \"%s\" not valid" % p)
  return idx 

def parse_path(pth):
  p = pth.split("/")
  if (len(p) != 3):
    raise PathError("Path \"%s\" is not valid" % pth)
  p = [v.strip() for v in p]
  try:
    if (p[0][-1] == "'"):
      p = p[:-1]
    acc = int(p[0])
    assert (acc >= 0)
  except:
    raise AccountError("\"%s\" is not a valid account" % p[0])
  try:
    chg = int(p[1])
    assert (chg == int(bool(chg)))
  except:
    raise ChangeError("\"%s\" is not a valid change identifier" % p[1])
  try:
    idx = int(p[2])
    assert (idx >= 0)
  except:
    raise AddressError("\"%s\" is not a valid address index" % p[2])
  return (acc, chg, idx)

def parse_network_byte(p):
  try:
    nw = int(p)
    assert (0 <= nw <= 255)
  except:
    raise NetworkError("Network byte \"%s\" not valid" % p)
  return nw
