import mmh3
from bitarray import bitarray


class BloomFilter:
    """Bloom Filter impl using murmurhash3"""

    def __init__(self, size=0, no_hash_fns=0) -> None:
        self.k = no_hash_fns
        self.size = size
        self.bitvector = bitarray(self.size)
        self.bitvector.setall(False)

    def hash(self, string: str) -> list:
        """Creating k hashes"""
        hash_arr = []
        offset = 0
        for _ in range(self.k + 1):
            _hash = mmh3.hash(string, offset)
            hash_arr.append(abs((_hash) % self.size))
            offset += 5
        return hash_arr

    def add(self, string: str) -> None:
        """Add element to bloom filter"""
        hashes = self.hash(string)
        for h in hashes:
            self.bitvector[h] = True

    def query(self, string: str) -> bool:
        """Query an element in bloom filter"""
        hashes = self.hash(string)
        for h in hashes:
            if self.bitvector[h] is not True:
                return False
        return True

    def clear(self) -> None:
        """Reset the bloom filter"""
        self.bitvector.setall(False)
