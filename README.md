# Introduction

The **stealth-key-tool** package is a high level wrapper around some of
the most critical functionality needed for heirarchical deterministic (HD)
wallets.  The primary goal of this package is to provide a simple means to
derive private keys, addresses, and other essential information from HD
mnemonics (typically 12, 18, or 24 word secret phrases).

## Key Functionalities

* Address derivation from any secret phrase for any coin according to BIP44.
* Public and private key derivation, suitable for import (e.g. WIF).
* **New**: Secret phrase generation and validation according to BIP39.
* Minimal dependencies and open source for better security.

## Example Use Case

You had your favorite coin on a hardware wallet, but it
stopped being supported, you need the private key to import into a mobile
wallet without compromising the rest of your coins on your hardware wallet.

Solution: just use **stealth-key-tool** on a secure, air-gapped machine and
exctract your key.

## Dependencies

The **stealth-key-tool** relies on
the [ecdsa](https://pypi.org/project/ecdsa/) package,
the [pycryptodome](http://pycryptodome.readthedocs.io/) package,
and is subject to security considerations therein. Please see especially the
advice [here](https://pypi.org/project/ecdsa/#Security).

## README Overview

This README is divided into three parts. The first part covers the basics of
HD wallets necessary to use this package. The second part describes the use
of the **stealth-key-tool.py** utility. Finally, the third part explains
the **stealth_key_tool** API (notice dashes versus underscores in the names
of the utility and package).


# HD Wallet Basics

In general this README assumes that the reader is either
(a) an expert in HD wallets, or (b) doesn't care how they work
and is getting help from and expert. For the latter type of
user: please remember to **NEVER SHARE your mnemonic with anyone**.

That said, any user of the **stealth-key-tool.py** utility must have a
rudimentary understanding of a couple of HD wallet basics.
First, HD wallets are created from a mnemonic. This mnemonic can be used
to derive practically unlimited addresses, each of which belongs an
account, and can either be a change address or a public address,
which is known in HD wallet parlance as an "external address".

Any address in the heirarchy of an HD wallet is expressed as a so-called
"path" or "chain". The conceptually "first" address of an HD wallet has
the following path:

```
m/44'/125'/0'/0/0
```

In this path, the apostrophes (`'`) have meanings that are beyond the scope
of this README. For our purposes, the user is advised to simply ignore
them, although they will be included in this discussion to ensure technical
precision. The leftmost `m` amounts to a visual cue that indicates the start
of the path. The `44'` never changes. The `125'` indicates the coin is
XST (this is the **stealth-key-tool**, after all). Each coin will have
a different number in this position. For example, instead of `125'`,
BTC uses `0'` here.

When limited to a single coin (like XST), the part of the path that changes
for the user are the last three elements, separated by forward slashes (`/`).
Here, this part of the path is:

```
0'/0/0
```

In this part, the leftmost zero (`0'`) indicates the account. Numbering starts
at 0, so this is the "first" account. The middle zero indicates that this
is an external address intended to be shared with others, as when withdrawing
from an exchange. This middle number is limited to `0` or `1`, the latter
of which indicates it is a "change" address, termed an "internal" address.
The rightmost `0` is the address identifier, typically called the
"address index".

Any change to the path gives a new and completely unpredictable address.

Although crude, the following ASCII-art hopes to illustrate the heirarchical
nature of HD wallets by showing the relationship of several paths, each
represented only by its last three identifiers (account/change/address).

```
 -> 0'/0/0 -> 0'/0/1 -> 0'/0/2
|   \
|    -> 0'/1/0 -> 0'/1/1 -> 0'/1/2
|
 -> 1'/0/0 -> 1'/0/1 -> 1'/0/2
    \
     -> 1'/1/0 -> 1'/1/1 -> 1'/1/2
```

It is important to highlight that each path in this heirarchy corresponds to a
unique address, completely unpredictable given knowledge of the other
addresses in the heirarchy.

For further understanding of HD wallets, a good place to start is with
Ledger's excellent
[writeup](https://www.ledger.com/academy/crypto/what-are-hierarchical-deterministic-hd-wallets).
For even deeper inquiry, the user is encouraged to read and understand
[BIP-0032](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki),
[BIP-0039](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), and
[BIP-0044](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki).

# stealth-key-tool.py

The **stealth-key-tool.py** utility is a command line (CLI) driven application
that takes a mnemonic as user input and derives cryptographic keypairs
that are then used to generate information, using simple commands.

## Preliminary Advice

**WARNING**: Never share any of the follwing:

* Your **mnemonic** (aka "secret phrase", aka "seed phrase")
* The **extended private key** (from the `xprv` command )
* The **hex private key** (from the `prv` command)
* The **WIF private key** (from the `wif` command)

Furthermore, one should be exceedingly careful about sharing an account's
extended public key (from the `xpub` command).

*If you have any doubts whether you should share the
extended public key, then don't share it.*

## Startup

When starting up, you will be prompted for the mnemonic (called the
"secret phrase" in the utility). By default, this input will be hidden.
To see what you type when you enter the mnemonic, hit enter before typing
the mnemonic, and you will be prompted again, this time with the ability
to see the text.

Please note that he mnemonic is not verified in any way. 

## Command Input

After the user enters the mnemonic, the utility goes into the "command loop",
which is just a basic user interface where the user types simple commands
to alter the heirarchy (also called a "path", or "chain"),
or to output desired information.

### Command Summaries

#### User Requested Output Commands

* `gp` : prints the current HD path
* `addr` : prints the address for the current HD path
* `xpub` : prints the account's extended public key
* `xprv` : prints the account's extended private key (**NEVER SHARE**)
* `pub` : prints the address's compressed public key
* `prv` : prints the address's private key (**NEVER SHARE**)
* `upub` : prints the address's uncompressed public key
* `wif` : prints the account's private key in WIF format (**NEVER SHARE**)

#### Path Selection Commands

* `sc` : sets the coin identifier
* `sa` : sets the account identifier
* `++a` : increments the account index by 1
* `--a` : decrements the account index by 1
* `ext` : un-sets the change specifier to external (non-change) addresses
* `int` : sets the change specifier to internal (change) addresses
* `si` : sets the address index
* `++i` : increments the address index
* `--i` : decrements the address index
* `sp` : sets the path using the last three elements (account/change/address)

#### Coin Parameter Commands

* `sanb` : sets the network byte used to create addresses
* `swnb` : sets the network byte used to create wif strings
* `xst`  : sets the coin parameters to those for XST
* `btc`  : sets the coin parameters to those for BTC
* `eth`  : sets the coin parameters to those for ETH
* `ltc`  : sets the coin parameters to those for LTC
* `doge`  : sets the coin parameters to those for DOGE
* `ftc`  : sets the coin parameters to those for FTC
* `vtc`  : sets the coin parameters to those for VTC

#### BIP39 Commands

* `mwp` : makes a new word phrase compliant with BIP39 (English only)
* `vwp` : validates a BIP39 compliant word phrase (English only)

#### App Control Commands

* `h` : prints list of commands
* `q` : quits the utility


### Arguments

Several commands take arguments that may be entered on the same line as the
command itself. These commands start with an "s": `sa`, `si`, and `sp`.
The following input shows an example of how to set the path with `sp`:

```
sp 5'/1/4
```

Given the default purpose, and XST as the currency, this command sets the path to:

```
m/44'/125'/5'/1/4
```

The two BIP39 commands (`mwp` and `vwp`) also take arguments. The following
shows how to make a 24 word phrase:

```
mwp 24
```

The following shows validation of a 12 word phrase:

```
vwp mansion breeze nerve urban rare pluck apart earth truth truly wood high
```

### User requested output

Several commands will produce user requested output. In these cases,
the output will be written to
[standard out](https://en.wikipedia.org/wiki/Standard_streams#Standard_output_(stdout)),
meaning that if the output from the utility is re-directed to a file,
for example, highly sensitive information could be leaked. Sensitive
commands in this category are: `xprv`, `prv` and `wif`.
**Please be careful with these commands.**

Other commands that produce user requested output are
`addr`, `gp`, `xpub`, `pub`, `mwp`, and `vwp`.

For further discussion of the importance of user requested output,
please see the section titled "Scripting".

### Increment and Decrement

Several commands simply increment and decrement identifiers.
These are included for convenience and ease to type. An example where
this might be useful is if a user wants to generate a handful of unique
addresses but doesn't have the time or patience to write a script.
These commands are `++a`, `--a`, `++i`, and `--i`.

## Scripting

To make the **stealth-key-tool.py** useful in a workflow, it features
the `-S` and `-N` flags that allows use in semi-interactive and
non-interactive modes, respectively. These modes allow for scripting
of the utility using shell scripts.

### Semi-interactive mode

In semi-interactive mode (`-S`), the utility
will prompt for the mnemonic, allowing the user to manually enter it into
the command line. Once entered,
the mnemonic is written to
[*stderr*](https://en.wikipedia.org/wiki/Standard_streams#Standard_error_(stderr))
so that it may be checked. Afterwards, only user requested output is
produced. Semi-interactive mode allows scripting without the need to
save the mnemonic to a plain text file (i.e. the script).
**WARNING**: be careful not to save to a file
or share the output of *stderr* in semi-interactive mode.

### Non-interactive mode

In non-interactive mode (`-N`), no option is given to the user
to hide the mnemonic upon entry and only user requested output is
produced. In this case, the mnemonic would need to be included in the script.

For scripting, semi-interactive mode (`-S`) is recommended if possible.

### Example bash script

As an example, here is a shell script that prints the
first four change addresses of the fifth account (account number 4)
for the mnemonic `some random words`, using semi-interactive mode:

```
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
```

Given the mnemonic `some random words`, the output of this script would be
 
```
SBmb6Zm9DTrXMTfYTDou5g5c72YBVntp6M
S6kyXjua5PsQRuTKmzJkuA3MVghba9gGrn
RxqKUDm45CBmLDwF7cympTCDkfSedx4op6
SKexTQxDywQi2FAxpo7tBtfWbZsWDhQwJo
```

This script is called "semi-interactive.bash" and is found in the "examples"
directory of the source distribution. A script with nearly identical
functionality that runs in non-interactive mode is also in
the "examples" directory as "non-interactive.bash".


# The API

The **stealth_key_tool** API exposes several high-level functions that
simplify the most common tasks related to working with HD wallets.

**keccak_256(...)**

```
keccak_256(message) -> Crypto.Hash.keccak.Keccak_Hash
```

Takes message as `bytes` and returns a
[pycryptodome](http://pycryptodome.readthedocs.io/)
`Crypto.Hash.keccak.Keccak_Hash`
object initialized and updated with the message.


**get_currency(...)**

```
get_currency(ticker) -> Currency
```

Takes a ticker as a `str` and returns a new instance of `Currency`
with the following attributes:

* *name* : `str` representing the currency name
* *ticker* : `str` representing the currency ticker
* *coin* : `int` representing the currency coin id
* *addr_net_byte* : `int` representing the address network byte
* *wif_net_byte* : `int` representing the wif network byte
* *get_address* : `function` *(key) -> str*
* *get_copy* : `function` *() -> Currency*

Available currencies are "XST", "BTC", "ETH", "LTC", "DOGE", "FTC", and "VTC".

The returned `Currency` object can be modified without influencing
the default currencies obtained by this function.


**seed_from_mnemonic(...)**

```
seed_from_mnemonic(mnemonic, salt="") -> bytes
```

Takes the mnemonic phrase as a `str` and optional salt as a `str` and
returns `bytes` representing the seed derived from the mnemonic.

**key_from_mnemonic(...)**

```
key_from_mnemonic(mnemonic, salt="") -> BIP32Key
```

Takes the mnemonic phrase as a `str` and optional salt as a `str` and
returns a private `BIP32Key` derived from the mnemonic.

**get_p2pkh_address(...)**

```
get_p2pkh_address(key, netbyte) -> str
```

Takes a `BIP32Key` and the network byte (62 for XST) to create
a pay-to-public-key-hash (p2pkh) address, returned as a `str`.

**get_eth_address(...)**

```
get_eth_address(key, netbyte=None) -> str
```

Takes a `BIP32Key` to create a checksummed ETH address as a `str`.
The `netbyte` argument is ignored if given to allow interchanging
of `get_*_address()` functions in a functional setting.


**get_child_key(...)**

```
 get_child_key(key, purpose=PURPOSE,
                    coin_type=None,
                    account=None,
                    change=None,
                    address_index=None) -> BIP32Key
```

Takes a `BIP32Key` and optional `int` arguments for the purpose,
coin type, account, change, and address index, to produce a new
child key returned as a `BIP32Key`. This function simplifies calculating
keys in the heirarchy by inferring from the argument list the heirarchical
level of the child key. *IMPORTANT*: the resulting child key will always
be hardened for purpose, coin type, and account.

**get_path(...)**

```
get_path(purpose, coin, account, change, index) -> str
```

Takes the purpose, coin, account, change, and address index as `int`s
and returns the full 6-part path (e.g. `m/44'/125'/0'/0/0`) as a `str`.

**get_wif(...)**

```
get_wif(key) -> str
```

Takes a `BIP32Key` and returns the private key in wallet import
format (WIF) as a `str`.


**parse_coin_id(...)**

```
parse_coin_id(p) -> int
```

Takes a `str` and attempts to interpret it as a coin identifier.
Throws a `CoinError` upon failure to interpret the input. The returned
value is an `int`. *IMPORTANT*: this function ignores any apostrophe
meant to indicate hardening and returns the identifier modulo
the hardening constant (0x80000000).

**parse_account_id(...)**

```
parse_account_id(p) -> int
```

Takes a `str` and attempts to interpret it as an account identifier.
Throws an `AccountError` upon failure to interpret the input. The returned
value is an `int`. *IMPORTANT*: this function ignores any apostrophe
meant to indicate hardening and returns the identifier modulo
the hardening constant (0x80000000).

**parse_address_index(...)**

```
parse_address_index(p) -> int
```

Takes a value and attempts to interpret it as an address index.
Throws an `AddressError` upon failure to interpret the input.
The returned value is an `int`.

**parse_path(...)**

```
parse_path(pth) -> tuple
```

Takes a `str` and attempts to parse it as an HD path. The path must have
three parts (e.g. `0'/0/0`) and evaluate to a valid path. If it fails,
it will throw one of `AccountError`, `ChangeError`, or `AddressError`
depending on the part of the path that is not valid. The returned `tuple`
has three `int` elements representing the account identifier, change
specifier, and address index. *IMPORTANT*: this function ignores any
apostrophe meant to indicate hardening and returns the account identifier
modulo the hardening constant (0x80000000).

**parse_network_byte(...)**

```
parse_network_byte(p) -> int
```

Takes a value and attempts to interpret it as a network byte.
Throws a `NetworkError` upon failure to interpret the input.
The returned value is an `int`.


**make_phrase_words(...)**

```
make_phrase_words(words, lang) -> list
```

Takes the number of words (12, 15, 18, 21, or 24) and the language,
(only `english` is supported currently) and returns a new,
random ordered set of words (`str`s) for use as a secret phrase mnemonic.

**check_phrase(...)**

```
check_phrase(phrase, lang) -> dict

Takes the phrase as a `str` (single space separated BIP39 words) and the
languange (only `english` is supported currently) and returns a
`dict` that reports the entropy, checksum, and validity.
```


# Copyright Notice

```
Copyright (c) 2022 2024, James Stroud

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```
