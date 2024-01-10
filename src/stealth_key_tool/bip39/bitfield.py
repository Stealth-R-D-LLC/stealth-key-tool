import math

def decompose(n, min_length=0):
  """
  Returns little endian decomposition of n as `bytes`.

  Zero-pads higher (more significant) bytes if required
  by `min_length`.
  """
  assert n >= 0
  a = bytearray()
  while n:
    q, r = divmod(n, 256)
    a.append(r)
    n = q
  for i in range(max(0, min_length - len(a))):
    a.append(0)
  return a

def reverse_byte(a):
  return [ 0x00, 0x80, 0x40, 0xc0, 0x20, 0xa0, 0x60, 0xe0,
           0x10, 0x90, 0x50, 0xd0, 0x30, 0xb0, 0x70, 0xf0,
           0x08, 0x88, 0x48, 0xc8, 0x28, 0xa8, 0x68, 0xe8,
           0x18, 0x98, 0x58, 0xd8, 0x38, 0xb8, 0x78, 0xf8,
           0x04, 0x84, 0x44, 0xc4, 0x24, 0xa4, 0x64, 0xe4,
           0x14, 0x94, 0x54, 0xd4, 0x34, 0xb4, 0x74, 0xf4,
           0x0c, 0x8c, 0x4c, 0xcc, 0x2c, 0xac, 0x6c, 0xec,
           0x1c, 0x9c, 0x5c, 0xdc, 0x3c, 0xbc, 0x7c, 0xfc,
           0x02, 0x82, 0x42, 0xc2, 0x22, 0xa2, 0x62, 0xe2,
           0x12, 0x92, 0x52, 0xd2, 0x32, 0xb2, 0x72, 0xf2,
           0x0a, 0x8a, 0x4a, 0xca, 0x2a, 0xaa, 0x6a, 0xea,
           0x1a, 0x9a, 0x5a, 0xda, 0x3a, 0xba, 0x7a, 0xfa,
           0x06, 0x86, 0x46, 0xc6, 0x26, 0xa6, 0x66, 0xe6,
           0x16, 0x96, 0x56, 0xd6, 0x36, 0xb6, 0x76, 0xf6,
           0x0e, 0x8e, 0x4e, 0xce, 0x2e, 0xae, 0x6e, 0xee,
           0x1e, 0x9e, 0x5e, 0xde, 0x3e, 0xbe, 0x7e, 0xfe,
           0x01, 0x81, 0x41, 0xc1, 0x21, 0xa1, 0x61, 0xe1,
           0x11, 0x91, 0x51, 0xd1, 0x31, 0xb1, 0x71, 0xf1,
           0x09, 0x89, 0x49, 0xc9, 0x29, 0xa9, 0x69, 0xe9,
           0x19, 0x99, 0x59, 0xd9, 0x39, 0xb9, 0x79, 0xf9,
           0x05, 0x85, 0x45, 0xc5, 0x25, 0xa5, 0x65, 0xe5,
           0x15, 0x95, 0x55, 0xd5, 0x35, 0xb5, 0x75, 0xf5,
           0x0d, 0x8d, 0x4d, 0xcd, 0x2d, 0xad, 0x6d, 0xed,
           0x1d, 0x9d, 0x5d, 0xdd, 0x3d, 0xbd, 0x7d, 0xfd,
           0x03, 0x83, 0x43, 0xc3, 0x23, 0xa3, 0x63, 0xe3,
           0x13, 0x93, 0x53, 0xd3, 0x33, 0xb3, 0x73, 0xf3,
           0x0b, 0x8b, 0x4b, 0xcb, 0x2b, 0xab, 0x6b, 0xeb,
           0x1b, 0x9b, 0x5b, 0xdb, 0x3b, 0xbb, 0x7b, 0xfb,
           0x07, 0x87, 0x47, 0xc7, 0x27, 0xa7, 0x67, 0xe7,
           0x17, 0x97, 0x57, 0xd7, 0x37, 0xb7, 0x77, 0xf7,
           0x0f, 0x8f, 0x4f, 0xcf, 0x2f, 0xaf, 0x6f, 0xef,
           0x1f, 0x9f, 0x5f, 0xdf, 0x3f, 0xbf, 0x7f, 0xff ][a]


class BitField:
  """
  A `BitField` is a view of an underlying `bytearray` data
  structure with `start` and `stop` limits. Limits are similar to
  slice limits for python data types (e.g. [5,6,7][1:3] -> [6,7],
  where 1 and 3 are the limits).

  The `data` parameter can either be an `int` which will be
  decomposed into a little-endian `bytearray`, or an iterable
  that can be converted to a `bytearray`.
  Limits apply even to data from decomposition.

  Bit ordering is conventional, where the LSB is in
  byte 0 at bit 0, etc. Binary representation (i.e. `__str__`)
  is conventional, with the LSB on the right and MSB on the left.
  Conventional ordering allows for simple normalization because the
  most significant byte will always be "right justified" where its
  LSB has the lowest index.

  Although accessible and mutable, the `data`, `start`, and
  `stop` attributes should be modified with care, as modifying
  any will change the view (and/or contents) of the underlying
  data structure.
  """
  def __init__(self, data, start=0, stop=None):
    try:
      i = iter(data)
      self.data = bytearray(i)
    except TypeError:
      if stop is None:
        min_length = 0
      else:
        min_length = int(math.ceil(abs(stop - start) / 8))
      self.data = decompose(data, min_length)
    self.start, self.stop = self.validate_limits(start, stop)
    self.end_index = self.stop - 1
  def __str__(self):
    result = [str(self.get_bit(i)) for i in range(self.size())]
    result.reverse()
    return "".join(result)
  def as_int(self):
    f = 1
    value = 0
    for i in range(self.size()):
      value += self.get_bit(i) * f
      f *= 2
    return value
  def size(self):
    return self.stop - self.start
  def validate_limits(self, start, stop=None):
    if start < 0:
      raise ValueError("start %d is negative" % start)
    data_len = 8 * len(self.data)
    if stop is None:
      stop = data_len
    elif stop > data_len:
      raise ValueError("stop %d exceeds data length" % stop)
    if stop < start:
      raise ValueError("stop %d less than start %d" % (stop, start))
    return start, stop
  def check_index(self, index):
    if (index < 0) or (index >= self.size()):
      return False
    return True
  def get_bit(self, index):
    if not self.check_index(index):
      raise ValueError("index %d is bad" % index)   
    byte_index, bit_shift = divmod(self.start + index, 8)
    byte = self.data[byte_index]
    return (byte & (1 << bit_shift)) >> bit_shift
  def copy(self):
    return BitField(self.data, self.start, self.stop)
  def get_slice(self, start_bit, stop_limit):
    # Some terms
    #   get_slice(2,13) --> ^
    #   
    #    byte 0   byte 1
    #   10101011 11001011
    #     bits   111111
    #   76543210 54321098
    #   ^^^^^^      ^^^^^
    #   ++++++~~ ***`````
    #
    #     fs = >>2 --> ~
    #    efs = >>5 --> `
    #     es = <<3 --> * 
    #     rs = <<6 --> +
    if not self.check_index(start_bit):
      raise ValueError("start limit %d is bad" % start_bit)
    end_bit = stop_limit - 1
    if not self.check_index(end_bit):
      raise ValueError("end_bit %d is bad" % end_bit)
    n_bits = stop_limit - start_bit
    start_bit += self.start
    stop_limit += self.start
    end_bit += self.start
    start_byte, fs = divmod(start_bit, 8)
    end_byte, efs = divmod(stop_limit, 8)
    es = 0 if (efs == 0) else (8 - efs)
    rs = 0 if (fs == 0) else (8 - fs)
    n_bytes = 1 + end_byte - start_byte
    if n_bytes == 0:
      return BitField([])
    elif n_bytes == 1:
      byte = self.data[start_byte]
      byte = (byte & (0xff >> es)) >> fs
      return BitField([byte], 0, n_bits)
    last_byte = self.data[start_byte]
    new = []
    finish_byte = end_byte if (efs == 0) else end_byte + 1
    for byte_index in range(start_byte + 1, finish_byte):
      this_byte = self.data[byte_index]
      if fs:
        byte = (last_byte >> fs) + ((this_byte & (0xff >> rs)) << rs)
      else:
        byte = last_byte
      new.append(byte)
      last_byte = this_byte
    byte_new = (last_byte & (0xff >> es)) >> fs
    new.append(byte_new)
    return BitField(new, 0, n_bits)
  def get_rslice(self, rstart_limit, rstop_limit):
    sz = self.size()
    start_limit = sz - rstop_limit
    stop_limit = sz - rstart_limit
    return self.get_slice(start_limit, stop_limit)
  def get_chunk(self, start_limit, stop_limit):
    return self.get_slice(start_limit, stop_limit).as_int()
  def get_rchunk(self, rstart_limit, rstop_limit):
    return self.get_rslice(rstart_limit, rstop_limit).as_int()
  def sliced(self, slice_size):
    n_bits = self.size()
    start = 0
    stop = min(n_bits, slice_size)
    new = []
    while start < stop:
      new.append(self.get_slice(start, stop))
      start += slice_size
      stop = min(n_bits, stop + slice_size)
    return new
  def rsliced(self, rslice_size):
    n_bits = self.size()
    start = 0
    stop = min(n_bits, rslice_size)
    new = []
    while start < stop:
      new.append(self.get_slice(n_bits - stop, n_bits - start))
      start += rslice_size
      stop = min(n_bits, stop + rslice_size)
    return new
  def chunked(self, chunk_size):
    return [v.as_int() for v in self.sliced(chunk_size)]
  def rchunked(self, rchunk_size):
    return [v.as_int() for v in self.rsliced(rchunk_size)]
  def normalized(self):
    return BitField(self.chunked(8), 0, self.size())
  def endian_swapped(self):
    new = self.normalized()
    new.data = new.data[::-1]
    return new
  def invert(self):
    self.data = [((~v) & 0xff) for v in self.data]
  def inverted(self):
    new = self.copy()
    new.invert()
    return new
  def strip(self):
    while (self.stop > self.start) and (self.get_bit(self.end_index) == 0):
      self.stop -= 1
      self.end_index -= 1
  def stripped(self):
    new = self.copy()
    new.strip()
    return new
  def catenate(self, other):
    new = self.chunked(8)
    n_bits = self.size()
    other_n_bits = other.size()
    if other_n_bits:
      overhang = n_bits % 8
      underhang = (8 - overhang) if overhang else 0
      if underhang:
        new[-1] += (other.get_chunk(0, underhang) << overhang)
      start = underhang
      while start < other_n_bits:
        stop = min(other_n_bits, start + 8)
        new.append(other.get_chunk(start, stop))
        start = stop
    return BitField(new, 0, n_bits + other_n_bits)
  def reversed(self):
    new = [reverse_byte(b) for b in self.data[::-1]]
    length = 8 * len(new)
    return BitField(new, length - self.stop, length - self.start)

def test():
  import sys
  bf = BitField([201, 185, 77, 189])
  assert str(bf) == "10111101010011011011100111001001"
  assert bf.get_bit(3) == 1
  assert bf.get_bit(5) == 0
  assert bf.get_bit(7) == 1
  assert bf.get_bit(9) == 0
  assert str(bf.get_slice(3, 4)) == "1"
  assert str(bf.get_slice(2, 5)) == "010"
  assert str(bf.get_slice(2, 13)) == "11001110010"
  assert str(bf.get_slice(7, 15)) == "01110011"
  assert str(bf.get_slice(3, 22)) == "0011011011100111001"
  assert str(bf.get_slice(3, 5)) == "01"
  assert bf.get_chunk(3, 5) == 1
  assert str(bf.get_slice(3, 7)) == "1001"
  assert bf.get_chunk(3, 7) == 9
  assert bf.get_rchunk(0, 6) == 47
  assert bf.get_rchunk(0, 11) == 1514
  assert bf.get_rchunk(11, 22) == 878
  assert ([str(v) for v in bf.sliced(11)] == 
          ['00111001001', '00110110111', '1011110101'])
  assert bf.chunked(11) == [457, 439, 757]
  assert ([str(v) for v in bf.rsliced(11)] ==
          ['10111101010', '01101101110', '0111001001'])
  assert bf.rchunked(11) == [1514, 878, 457]
  assert ([str(v) for v in bf.sliced(8)] ==
          ['11001001', '10111001', '01001101', '10111101'])
  assert bf.chunked(8) == [201, 185, 77, 189]
  assert ([str(v) for v in bf.sliced(7)] ==
          ['1001001', '1110011', '0110110', '1101010', '1011'])
  assert ([list(v.data) for v in bf.sliced(7)] ==
          [[73], [115, 0], [54, 0], [234, 0], [11]])
  assert [v.size() for v in bf.sliced(7)] == [7, 7, 7, 7, 4]
  assert bf.chunked(7) == [73, 115, 54, 106, 11]
  assert bf.as_int() == 3175987657
  assert str(bf.normalized()) == "10111101010011011011100111001001"
  assert str(bf.endian_swapped()) == "11001001101110010100110110111101"
  bfb = BitField([19, 11, 211], 1, 21)
  assert str(bfb) == "10011000010110001001"
  assert list(bfb.data) == [19, 11, 211]
  bf2 = bf.catenate(bfb)
  assert (str(bf2) ==
          "1001100001011000100110111101010011011011100111001001")
  assert list(bf2.data) == [201, 185, 77, 189, 137, 133, 9]
  mt = BitField([])
  assert list(mt.data) == []
  assert str(mt.catenate(bf)) == "10111101010011011011100111001001"
  assert str(bfb.catenate(mt)) == "10011000010110001001"
  intbf = BitField(6316041329636)
  assert (str(intbf) ==
          "000001011011111010010001011001100101101111100100")
  assert list(intbf.data) == [228, 91, 102, 145, 190, 5]
  assert intbf.size() == 48
  stripped = intbf.stripped()
  assert (str(stripped) ==
          "1011011111010010001011001100101101111100100")
  assert stripped.size() == 43
  inverted = stripped.inverted()
  assert (str(inverted) ==
          "0100100000101101110100110011010010000011011")
  assert (str(inverted.stripped()) ==
          "100100000101101110100110011010010000011011")
  assert (str(inverted.reversed()) ==
          "1101100000100101100110010111011010000010010")
  assert (str(BitField(3582200835639638158).reversed()) ==
          "0111000100011110000101100100001001110101000100010110110110001100")
  assert (str(BitField(1000615875044196781).reversed()) ==
          "1011010110000010000001010011110001101011011001110100011110110000")
  assert (str(BitField(43807708550511).reversed() ==
          "111101101010100000010111011000111110101111100100"))
  print("All tests passed.", file=sys.stderr)


if __name__ == "__main__":
  test()

