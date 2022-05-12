import math
from functools import reduce
from operator import add, mul
from typing import Iterator, List, Dict

import numpy as np
from bitarray import bitarray
from more_itertools import map_if, unzip
from succinct.poppy import Poppy
from tqdm import tqdm


class DAC:

    def __init__(self, values: Iterator[int]) -> None:

        vals = list(values)

        self._num_values = len(vals)

        self.__A = []
        self.__B = []
        self._levels, self._block_sizes = self.__optimize(vals, 0.05)
        self._original_bit_size = len(vals) * max(1, max(vals).bit_length())
        self._vbyte_bit_size = sum(map(lambda x: 8 * math.ceil(math.log2(x+1)/7), vals))

        for level in tqdm(range(self._levels), desc="Constructing optimal DAC."):

            current_block_size = self._block_sizes[level]

            # get current_block values and remaining bits
            A_i, A_j = list(map(list,
                                unzip(map(lambda x: (x & (2 ** current_block_size - 1), x >> current_block_size),
                                          vals))))

            # get continuation blocks
            continuation_bits = list(map_if(A_j, lambda x: x > 0, lambda x: 1, func_else=lambda x: 0))

            # store lower block_values
            # TODO: store in bitarray
            self.__A.append(A_i)

            # store continuation_bits except for last level
            if level < (self._levels - 1):
                self.__B.append(Poppy(bitarray(reduce(add, map(str, continuation_bits)))))

            # get non-zero values for next round
            vals = list(filter(lambda x: x > 0, A_j))

    @property
    def bit_length(self) -> int:
        """
        :return: Number of bits needed for DAC encoding of integer sequence.
        """

        total_continuation_bits = sum(map(lambda x: 1.05 * x._size, self.__B))
        total_block_bits = sum(reduce(mul, data) for data in zip(*[self._block_sizes, list(map(len, self.__A))]))

        return total_block_bits + total_continuation_bits

    @property
    def compression_ratios(self) -> Dict[str, float]:
        """
        :return: Ratio between size of uncompressed integer sequence and size of DAC encoded integer sequence.
        """

        return {"vbyte": self._vbyte_bit_size / self.bit_length,
                "fixed_width": self._original_bit_size / self.bit_length}

    @property
    def space_savings(self) -> Dict[str, float]:
        """
        :return: Ratio between size of uncompressed integer sequence and size of DAC encoded integer sequence.
        """

        return {"vbyte":   1.0 - self.bit_length / self._vbyte_bit_size,
                "fixed_width":     1.0 - self.bit_length / self._original_bit_size}

    @property
    def num_values(self) -> int:
        """
        :return: Number of integers in DAC encoded sequence.
        """

        return self._num_values

    @property
    def block_sizes(self) -> List[int]:
        """
        :return: Width of bit blocks.
        """
        return self._block_sizes

    @property
    def levels(self) -> int:
        """
        :return: Number of levels.
        """
        return self._levels

    def __len__(self) -> int:
        """
        :return: Number of integers in DAC encoded sequence.
        """

        return self._num_values

    def __iter__(self) -> Iterator[int]:
        """
        :return: Iterator over DAC encoded integer sequence.
        """

        for i in range(self._num_values):
            yield self[i]

    def __getitem__(self, k: int) -> int:
        """
        :param k: Index of an element in the DAC encoded integer sequence.
        :return: k-th element in the DAC encoded integer sequence.
        :raises IndexError: if k ∉ [0, ... , num_values)
        """
        if not (0 <= k < self._num_values):
            raise IndexError(f"Index %s ∉ [0,..,{self._num_values - 1}]." % k)

        item = 0

        for level in range(0, len(self.__A)):
            item += self.__A[level][k] << sum(self._block_sizes[0: level])

            if level >= len(self.__B):
                break
            elif isinstance(self.__B[level], Poppy):
                if self.__B[level][k]:
                    k = self.__B[level].rank(k) - 1
                else:
                    break
            else:
                break

        return item

    def __optimize(self, sequence: List[int], x=0.05):
        """
        @article{Ladra2011,
                 author = {Ladra, Susana},
                 institution = {Universidade da Coru{\~{n}}a},
                 isbn = {5626895531},
                 pages = {272},
                 title = {{Algorithms and Compressed Data Structures for Information Retrieval}},
                 type = {Phd Thesis},
                 year = {2011}
        }

        https://github.com/sladra/DACs/blob/master/src/dacs.c
        """

        M = max(sequence)
        m = math.floor(math.log2(M))

        # way faster than: fc = [len(list(filter(lambda e: e < 2**i, sequence))) for i in range(0, m + 2)]
        fc = [0] * (m + 2)
        hist = np.unique(list(map(lambda x: max(1, int(x).bit_length()), sequence)), return_counts=True)
        for i, c in tqdm(zip(hist[0], hist[1]), desc="Computing cumulative frequencies."):
            fc[i - 1] = c
        fc = np.cumsum(fc).astype(int).tolist()

        s = [0] * (m + 1)
        l = [0] * (m + 1)
        b = [0] * (m + 1)

        for t in tqdm(reversed(range(0, m + 1)), desc="Computing optimal block sizes."):
            minSize = math.inf
            minPos = m

            for i in reversed(range(t + 1, m)):
                currentSize = s[i] + (fc[m + 1] - fc[t]) * (i - t + 1 + x)
                if minSize > currentSize:
                    minSize = currentSize
                    minPos = i

            if minSize < (fc[m + 1] - fc[t]) * (m - t + 1):
                s[t] = minSize
                l[t] = l[minPos] + 1
                b[t] = minPos - t
            else:
                s[t] = (fc[m + 1] - fc[t]) * (m - t + 1)
                l[t] = 1
                b[t] = (m - t + 1)

        L = l[0]
        kvalues = [0] * L
        t = 0

        for k in range(0, L):
            kvalues[k] = b[t]
            t = t + b[t]

        return L, kvalues