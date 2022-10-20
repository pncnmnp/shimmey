import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size=0, no_hash_fns=0):
        self.k = no_hash_fns
        self.size = size
        self.bitvector = bitarray(self.size)
        self.bitvector.setall(False)

    def hash(self, string):
        hash_arr = []
        offset = 0
        for _ in range(self.k + 1):
            _hash = mmh3.hash(string, offset)
            hash_arr.append(abs((_hash) % self.size))
            offset += 5
        return hash_arr

    def add(self, string):
        hashes = self.hash(string)
        for h in hashes:
            self.bitvector[h] = True

    def query(self, string):
        hashes = self.hash(string)
        for h in hashes:
            if self.bitvector[h] != True:
                return False
        return True

    def clear(self):
        self.bitvector.setall(False)
