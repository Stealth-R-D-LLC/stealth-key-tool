# Password based key-derivation function - PBKDF2

http://en.wikipedia.org/wiki/PBKDF2

To use this in your application, simply download the
module, then run something like this:

    import pbkdf2
    import hashlib
    import os

    >>> pbkdf2.pbkdf2(hashlib.sha256, b"password1", os.urandom(32), 32000, 16)
    b'\x1e\xa9\xa0\xa7N\xf6\x97\x9ce\x94ZpU\x03n?'


**PBKDF2, from PKCS #5 v2.0**  
<http://tools.ietf.org/html/rfc2898>

**For proper usage, see NIST Special Publication 800-132**  
<http://csrc.nist.gov/publications/nistpubs/800-132/nist-sp800-132.pdf>

## Arguments

 - `digestmod`

    a crypographic hash constructor, such as `hashlib.sha256`
    which will be used as an argument to the hmac function.
    Note that the performance difference between sha1 and
    sha256 is not very big. New applications should choose
    sha256 or better.

 - `password` (bytes)

    The arbitrary-length password (passphrase). Note that this
    is a bytes() object, not a string. If your password is a
    utf-8 string, simple put `password.encode()`.

 - `salt` (bytes)

    A bunch of random bytes, generated using a cryptographically
    strong random number generator (such as `os.urandom()`). NIST
    recommend the salt be _at least_ 128bits (16 bytes) long.

 - `count` (int >= 1)

    The iteration count. Set this value as large as you can
    tolerate. NIST recommend that the absolute minimum value
    be 1000. However, it should generally be in the range of
    tens of thousands, or however many cause about a half-second
    delay to the user.

 - `dk_length` (int >= 1)

    The lenght of the desired key in bytes. This doesn't need
    to be the same size as the hash functions digest size, but
    it makes sense to use a larger digest hash function if your
    key size is large. 

## Copyright Notice

    Copyright (c) 2011, Stefano Palazzo <stefano.palazzo@gmail.com>

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
