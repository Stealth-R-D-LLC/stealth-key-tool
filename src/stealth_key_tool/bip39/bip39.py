import hashlib
import math
import secrets
import binascii

from .bitfield import BitField

from .english import english

STANDARD_ENTROPIES = {12: 128, 15: 160, 18: 192, 21: 224, 24: 256}

ENGLISH = "english"

languages = {ENGLISH: english}


def make_phrase_words(words, lang=ENGLISH):
  # allow only standard lengths for now
  if words not in STANDARD_ENTROPIES:
    msg = "Number of words (%s) is bad." % (words,)
    raise ValueError(msg)

  bits = STANDARD_ENTROPIES[words]

  word_list = languages[lang]["word_list"]

  # generalize with some quick math
  bytes_ent = int(math.ceil(bits / 8))
  bits_ent = bytes_ent * 8
  n_words = int(math.ceil(bits_ent / 11))
  # TODO: is this floor or ceil?
  bits_ck = int(math.ceil(bits_ent / 32))
  n_bits = bits_ent + bits_ck
  ck_unused = 8 - bits_ck

  # sanity check for now
  # assert n_words == words

  # generate the secret
  secret = secrets.token_bytes(bytes_ent)

  # checksum
  h = hashlib.sha256(secret).digest()

  # BIP39 standard weirdly interprets the bytes big-endian
  #   1. zero the unused bits of ck
  #      (big-endian treatment means ck is left-justified)
  ck = h[0] & (0xff << ck_unused)
  #   2. insert ck as the lower byte
  #   3. and swap endianness of the secret
  checked = bytes([ck]) + secret[::-1]
  #   4. trim off the unused low bits in ck
  bf = BitField(checked, ck_unused, ck_unused + n_bits)
  #   5. take 11 bit chunks starting from the left (reverse chunked)
  return [word_list[i] for i in bf.rchunked(11)]

def check_phrase(phrase, lang=ENGLISH):
  words = phrase.split(" ")
  lookup = languages[lang]["lookup"]

  n_words = len(words)

  # allow only standard lengths for now
  bits_ent = STANDARD_ENTROPIES[n_words]
  # TODO: is this floor or ceil?
  bits_ck = int(math.ceil(bits_ent / 32))

  data = BitField([])

  for word in words:
    value = lookup[word]
    bfw = BitField(value, 0, 11)
    # prepend bits from new words, to be reversed later (rchunked)
    data = bfw.catenate(data)

  checksum = data.get_slice(0, bits_ck)
  entropy = data.get_slice(bits_ck, data.size())

  entropy_bytes = bytes(entropy.rchunked(8))

  ck = checksum.as_int()

  h = hashlib.sha256(entropy_bytes).digest()
  shift = 8 - bits_ck
  h_ck = h[0] >> shift

  is_valid = (ck == h_ck)

  entropy_hex = binascii.hexlify(entropy_bytes).decode("utf-8")

  return { "words": words,
           "bits entropy": bits_ent,
           "entropy": str(entropy),
           "entropy hex": entropy_hex,
           "checksum": str(checksum),
           "checksum value": ck,
           "data": str(data),
           "valid": is_valid }

def create_new_phrase(n):
  words = make_phrase_words(15)
  phrase = " ".join(words)
  result = check_phrase(phrase)
  for k, v in result.items():
    print("%s: %s" % (k, v))

def test(n_tests):
  import sys
  for n in STANDARD_ENTROPIES:
    for i in range(n_tests):
      if not i % (n_tests//10):
        print("Done: %d of %d for %d word test" % (i, n_tests, n),
              file=sys.stderr)
      words = make_phrase_words(n)
      phrase = " ".join(words)
      result = check_phrase(phrase)
      if not result['valid']:
        print(phrase, file=sys.stderr)
        print("Phrase is valid: %s" % result['valid'], file=sys.stderr)
        print("Checksum: %d" % result['checksum'], file=sys.stderr)
        print("Checksum (binary): %s" % format(result['checksum'], 'b'),
              file=sys.stderr)
        print("Checksum bits: %s" % result['checksum bits'], file=sys.stderr)
        raise SystemExit
  print("All tests passed.", file=sys.stderr)

if __name__ == "__main__":
  # create_new_phrase(15)
  test(1000)
