# BIP39

## Basic Usage

To use this in your application, simply download the module, then run something like this:

    >>> import json
    >>> from bip39 import ENGLISH, make_phrase_words, check_phrase
    >>> words = make_phrase_words(24, ENGLISH)
    >>> print(json.dumps(check_phrase(" ".join(words)), indent=2))

### Arguments to `make_phrase_words()`

- **words** (`int`)

    One of 12, 15, 18, 21, or 24.

- **language** (`str`)

    String naming the language to use (e.g. "english").

    At the moment, only English is supported.

### Argument to `check_phrase()`

- **phrase** (`str`)

    list of bip39 words, joined by single spaces, e.g.:

        impose segment stay odor invite brush fresh tilt west nest camera crisp

## BitField

This module also exposes the convenient but incomplete little-endian **BitField** class, with LSB in the lowest bit of the lowest byte.

The **BitField** class is implemented for data compactness and speed.

### Some example usage

Create a **BitField**:

    >>> bf1 = BitField([0xfb, 0xfb, 0x82])

String representation is a string of bits, LSB on the right (basically a binary number):

    >>> print(bf1)
    100000101111101111111011

**BitFields** can be created from integers, implicitly sized as a multiple of 8:

    >>> bf2 = BitField(924)
    >>> print(bf2)
    0000001110011100

Remove 0-valued high bits with `strip()` or `stripped()`, the latter makes a new **Bitfield**, the former modifies in place:

    >>> bf3 = bf2.stripped()
    >>> print(bf3)
    1110011100

Convert a **BitField** to an integer with `as_int()`:

    >>> bf2.as_int(), bf3.as_int()
    (924, 924)

The `start` and `stop` members allow for arbitrarily sized **BitFields**. The `start` and `stop` members denote boundaries (limits) similar to Pythonic slicing:

    >>> (bf2.start, bf2.stop), (bf3.start, bf3.stop)
    ((0, 16), (0, 10))
    >>> print(BitField(int("1011101", 2), start=1, stop=5))
    1110
    
Catenate one **BitField** to another with `catenate()` to make a new **BitField**, with the catenated bits appended to the higher-indexed bytes.

    >>> print(bf3, bf2, bf2.catenate(bf3))
    1110011100 0000001110011100 11100111000000001110011100

The `size()` method returns the number of bits in the **BitField**:

    >>> bf1.size()
    24

Check if a bit index is valid with `check_index()` without doing math or using comparisons:

    >>> bf1.check_index(23)
    True
    >>> bf1.check_index(24)
    False

Access individual bits by index with `get_bit()`:

    >>> print(bf1.get_bit(23))
    1

Create a new **BitField** by getting a slice with `get_slice()`:

    >>> print(bf1.get_slice(0, 5))
    11011

Get parts of a **BitField** as integers with `get_chunk()`:

    >>> int("11011", 2), bf1.get_chunk(0, 5)
    (27, 27)

A **BitField** `sliced()` makes a `list` of new **BitFields**:

    >>> [str(v) for v in bf1.sliced(6)]
    ['111011', '101111', '101111', '100000']

A **BitField** `chunked()` is a `list` of integers:

    >>> [format(v, "06b") for v in bf1.chunked(6)]
    ['111011', '101111', '101111', '100000']

Chunking follows little-endianness, where lower-indexed chunks come from lower-indexed bits in the **BitField**:

    >>> [format(v, "06b") for v in bf1.chunked(6)][::-1]
    ['100000', '101111', '101111', '111011']
    >>> print(bf1)
    100000101111101111111011

Chunking can be done in reverse with `rchunked()`, but chunking in reverse with `rchunked()` is not the same as reversing chunks:

    >>> [format(v, "05b") for v in bf1.rchunked(5)]
    ['10000', '01011', '11101', '11111', '01011']
    >>> [format(v, "05b") for v in bf1.chunked(5)][::-1]
    ['01000', '00101', '11110', '11111', '11011']

Slicing with `sliced()` takes exact bitwise slices, unlike chunking that yields numbers that don't have any formal bit boundaries:

    >>> [str(v) for v in bf1.rsliced(5)]
    ['10000', '01011', '11101', '11111', '1011']
    

Invert all the bits with `invert()`, which modifies in place, or `inverted()`, which creates a new **BitField**:

    >>> str(bf3), str(bf3.inverted())
    ('1110011100', '0001100011')

Make a carbon copy with `copy()`:

    >>> str(bf3.copy())
    '1110011100'

To accomodate applications that conceptualize data as big-endian (e.g. Bitcoin's bip39), `endian_swapped()` makes a new **BitField** with the underlying data byte-wise backwards.

    >>> str(bf1), str(bf1.endian_swapped())
    ('100000101111101111111011', '111110111111101110000010')
    >>> list(bf1.data), list(bf1.endian_swapped().data)
    ([251, 251, 130], [130, 251, 251])
    
Swapping endianness doesn't reverse bits. To get full bitwise reversal, use `reversed()` to make a new **BitField**:

    >>> str(bf1)[::-1], str(bf1.reversed())
    ('110111111101111101000001', '110111111101111101000001')
