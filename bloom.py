import mmh3
from bitarray import bitarray


class BloomFilter:
    """A simple implementation of a bloom filter.

    Attributes:
        n -- the expected number of elements to be added
        to the filter. Used for number of bits allocated
        for the bitarray

        fp -- the false positive value the user is willing
        to tolerate.

        k -- the number of desired hash functions

    """

    def __init__(self, m=0, k=0):
        self.k = k
        self.m = m
        self.eltsAdded = 0
        self.bvector = bitarray(self.m)
        self.bvector.setall(False)

    # Calculates k number of hashes using
    # the murmur hash function
    def hash(self, string):
        hash_arr = []
        offset = 0
        for _ in range(self.k + 1):
            _hash = mmh3.hash(string, offset)
            hash_arr.append(abs((_hash) % self.m))
            offset += 5
        return hash_arr

    # Adds an element to the bloom filter
    def add(self, string):
        hashes = self.hash(string)
        for elt in hashes:
            self.bvector[elt] = True
        self.eltsAdded += len(hashes)

    # Queries for membership of element in the
    # bloom filter
    def query(self, string):
        hashes = self.hash(string)
        for elt in hashes:
            if self.bvector[elt] != True:
                return False
        return True

    # Clears the bloom filter and resets all
    # values in the bit vector to 0
    def clear(self):
        self.bvector.setall(False)
        self.eltsAdded = 0
