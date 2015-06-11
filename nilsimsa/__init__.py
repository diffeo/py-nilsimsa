"""
Purpose: Class and helper functions to compute and compare nilsimsa digests.

The Nilsimsa hash is a locality senstive hash function, generally
similar documents will have similar Nilsimsa digests.
The hamming distance between the digests can be used to approximate
the similarity between documents.
For further information consult http://en.wikipedia.org/wiki/Nilsimsa_Hash
and the references (particularly Damiani et al.)

Implementation details:
Nilsimsa class takes in a data paramater that can be an iterator over chunks of text or a text string.
Calling the methods hexdigest() and digest() give the nilsimsa
digest of the input data.
The helper function compare_digests takes in two digests and computes the Nilsimsa score.

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.
"""

import sys

if sys.version_info[0] >= 3:
    PY3 = True
    text_type = str
    range_ = range
else:
    PY3 = False
    text_type = unicode
    range_ = xrange

def is_iterable_non_string(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, (bytes, text_type))

# Constant used in tran53 hash function, contains values 0 <= x <= 255
# see implementation of tran_hash() below for details on usage
TRAN = [ord(x) for x in
    "\x02\xD6\x9E\x6F\xF9\x1D\x04\xAB\xD0\x22\x16\x1F\xD8\x73\xA1\xAC"\
    "\x3B\x70\x62\x96\x1E\x6E\x8F\x39\x9D\x05\x14\x4A\xA6\xBE\xAE\x0E"\
    "\xCF\xB9\x9C\x9A\xC7\x68\x13\xE1\x2D\xA4\xEB\x51\x8D\x64\x6B\x50"\
    "\x23\x80\x03\x41\xEC\xBB\x71\xCC\x7A\x86\x7F\x98\xF2\x36\x5E\xEE"\
    "\x8E\xCE\x4F\xB8\x32\xB6\x5F\x59\xDC\x1B\x31\x4C\x7B\xF0\x63\x01"\
    "\x6C\xBA\x07\xE8\x12\x77\x49\x3C\xDA\x46\xFE\x2F\x79\x1C\x9B\x30"\
    "\xE3\x00\x06\x7E\x2E\x0F\x38\x33\x21\xAD\xA5\x54\xCA\xA7\x29\xFC"\
    "\x5A\x47\x69\x7D\xC5\x95\xB5\xF4\x0B\x90\xA3\x81\x6D\x25\x55\x35"\
    "\xF5\x75\x74\x0A\x26\xBF\x19\x5C\x1A\xC6\xFF\x99\x5D\x84\xAA\x66"\
    "\x3E\xAF\x78\xB3\x20\x43\xC1\xED\x24\xEA\xE6\x3F\x18\xF3\xA0\x42"\
    "\x57\x08\x53\x60\xC3\xC0\x83\x40\x82\xD7\x09\xBD\x44\x2A\x67\xA8"\
    "\x93\xE0\xC2\x56\x9F\xD9\xDD\x85\x15\xB4\x8A\x27\x28\x92\x76\xDE"\
    "\xEF\xF8\xB2\xB7\xC9\x3D\x45\x94\x4B\x11\x0D\x65\xD5\x34\x8B\x91"\
    "\x0C\xFA\x87\xE9\x7C\x5B\xB1\x4D\xE5\xD4\xCB\x10\xA2\x17\x89\xBC"\
    "\xDB\xB0\xE2\x97\x88\x52\xF7\x48\xD3\x61\x2C\x3A\x2B\xD1\x8C\xFB"\
    "\xF1\xCD\xE4\x6A\xE7\xA9\xFD\xC4\x37\xC8\xD2\xF6\xDF\x58\x72\x4E"]

# Shortcut to compute the Hamming distance between two bit vector representations of integers
# POPC - population count, POPC[x] = number of 1's in binary representation of x
# POPC[a ^b] = hamming distance from a to b
POPC = [ord(x) for x in
    "\x00\x01\x01\x02\x01\x02\x02\x03\x01\x02\x02\x03\x02\x03\x03\x04"\
    "\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05"\
    "\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05"\
    "\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06"\
    "\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05"\
    "\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06"\
    "\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06"\
    "\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07"\
    "\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05"\
    "\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06"\
    "\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06"\
    "\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07"\
    "\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06"\
    "\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07"\
    "\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07"\
    "\x04\x05\x05\x06\x05\x06\x06\x07\x05\x06\x06\x07\x06\x07\x07\x08"]


class Nilsimsa(object):
    """
    computes the nilsimsa has of an input data block, which can be an
    iterator over chunks, with each chunk corresponding to a block of text
    """
    def __init__(self, data = None):
        # data comes as an iterator over chunks, which are an iterator over characters
        self.complete = False       # flag to prevent re-computation
        self.num_char = 0           # Number of characters that we have come across
        self.acc = [0] * 256        # 256-bit vector to hold the results of the digest
        self.window = []            # holds the window of the last 4 characters
        if data:
            if is_iterable_non_string(data):
                for chunk in data:
                    self.process(chunk)
            elif isinstance(data, (bytes, text_type)):
                self.process(data)
            else:
                raise TypeError("Excpected string, iterable or None, got {}"
                                    .format(type(data)))

    def tran_hash(self, a, b, c, n):
        """implementation of the tran53 hash function"""
        return (((TRAN[(a+n)&255]^TRAN[b]*(n+n+1))+TRAN[(c)^TRAN[n]])&255)

    def process(self, chunk):
        """
        computes the hash of all of the trigrams in the chunk using a window
        of length 5
        """
        if isinstance(chunk, text_type):
            chunk = chunk.encode('utf-8')

        # chunk is a byte string
        for char in chunk:
            self.num_char += 1
            if PY3:
                # In Python 3, iterating over bytes yields integers
                c = char
            else:
                c = ord(char)
            if len(self.window) > 1:            # seen at least three characters
                self.acc[self.tran_hash(c, self.window[0], self.window[1], 0)] += 1
            if len(self.window) > 2:            # seen at least four characters
                self.acc[self.tran_hash(c, self.window[0], self.window[2], 1)] += 1
                self.acc[self.tran_hash(c, self.window[1], self.window[2], 2)] += 1
            if len(self.window) > 3:            # have a full window
                self.acc[self.tran_hash(c, self.window[0], self.window[3], 3)] += 1
                self.acc[self.tran_hash(c, self.window[1], self.window[3], 4)] += 1
                self.acc[self.tran_hash(c, self.window[2], self.window[3], 5)] += 1
                # duplicate hashes, used to maintain 8 trigrams per character
                self.acc[self.tran_hash(self.window[3], self.window[0], c, 6)] += 1
                self.acc[self.tran_hash(self.window[3], self.window[2], c, 7)] += 1

            # add current character to the window, remove the previous character
            if len(self.window) < 4:
                self.window = [c] + self.window
            else:
                self.window = [c] + self.window[:3]


    def compute_digest(self):
        """
        using a threshold (mean of the accumulator), computes the nilsimsa digest
        after completion sets complete flag to true and stores result in
        self.digest
        """
        num_trigrams = 0
        if self.num_char == 3:          # 3 chars -> 1 trigram
            num_trigrams = 1
        elif self.num_char == 4:        # 4 chars -> 4 trigrams
            num_trigrams = 4
        elif self.num_char > 4:         # > 4 chars -> 8 for each char
            num_trigrams = 8 * self.num_char - 28

        # threshhold is the mean of the acc buckets
        threshold = num_trigrams / 256.0

        digest = [0] * 32
        for i in range(256):
            if self.acc[i] > threshold:
                digest[i >> 3] += 1 << (i & 7)      # equivalent to i/8, 2**(i mod 7)

        self.complete = True            # set flag to True
        self.digest = digest[::-1]      # store result in digest, reversed

    def digest(self):
        """
        returns the digest, if it has not been computed, calls compute_digest
        """
        if not self.complete:
            self.compute_digest()
        return self.digest

    def hexdigest(self):
        """
        computes the hex of the digest
        """
        if not self.complete:
            self.compute_digest()

        return ''.join('%02x'%i for i in self.digest)

    def __str__(self):
        """convenience function"""
        return self.hexdigest()

    def from_file(self, fname):
        """read in a file and compute digest"""
        f = open(fname, "rb")
        data = f.read()
        self.update(data)
        f.close()

    def compare(self, digest_2, is_hex = False):
        """
        returns difference between the nilsimsa digests between the current
        object and a given digest
        """
        if not self.complete:
            digest = self.compute_digest()
        else:
            digest = self.digest

        # convert hex string to list of ints
        if is_hex:
            digest_2 = convert_hex_to_ints(digest_2)

        bit_diff = 0
        for i in range(len(digest)):
            bit_diff += POPC[digest[i] ^ digest_2[i]]           #computes the bit diff between the i'th position of the digests

        return 128 - bit_diff       # -128 <= nilsimsa score <= 128


def convert_hex_to_ints(hexdigest):
    return [int(hexdigest[i:i+2], 16) for i in range(0, 63, 2)]

def compare_digests(digest_1, digest_2, is_hex_1=True, is_hex_2=True, threshold=None):
    """
    computes bit difference between two nilsisa digests
    takes params for format, default is hex string but can accept list
    of 32 length ints
    Optimized method originally from https://gist.github.com/michelp/6255490

    If `threshold` is set, and the comparison will be less than
    `threshold`, then bail out early and return a value just below the
    threshold.  This is a speed optimization that accelerates
    comparisons of very different items; e.g. tests show a ~20-30% speed
    up.  `threshold` must be an integer in the range [-128, 128].

    """
    # if we have both hexes use optimized method
    if threshold is not None:
        threshold -= 128
        threshold *= -1
    if is_hex_1 and is_hex_2:
        bits =  0
        for i in range_(0, 63, 2):
            bits += POPC[255 & int(digest_1[i:i+2], 16) ^ int(digest_2[i:i+2], 16)]
            if threshold is not None and bits > threshold: break
        return 128 - bits
    else:
        # at least one of the inputs is a list of unsigned ints
        if is_hex_1:  digest_1 = convert_hex_to_ints(digest_1)
        if is_hex_2:  digest_2 = convert_hex_to_ints(digest_2)
        bit_diff = 0
        for i in range(len(digest_1)):
            bit_diff += POPC[255 & digest_1[i] ^ digest_2[i]]
            if threshold is not None and bit_diff > threshold: break
        return 128 - bit_diff

