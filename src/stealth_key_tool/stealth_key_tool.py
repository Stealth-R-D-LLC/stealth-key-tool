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

import base64
import hashlib

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

# net byte values
NET_XST = 62
NET_BTC = 0
NET_TEST = 111

# wif encoding
WIF_PREFIX_XST = bytes([0xbe])  # 190
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

# generalized for any network byte
def get_address(key, netbyte):
  vh160 = netbyte.to_bytes(1, "big") + key.Identifier()
  return Base58.check_encode(vh160)

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

def get_wif(key):
  raw = WIF_PREFIX_XST + key.k.to_string() + WIF_COMPRESSED
  return Base58.check_encode(raw)

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
