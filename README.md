# pyDAC

[![Upload Python Package](https://github.com/rmrschub/pyDAC/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/rmrschub/pyDAC/actions/workflows/pypi-publish.yml)

pyDAC (python Directly Addressable Codes) offers a variable-length encoding scheme for (unsigned) integers with random access to any element of the encoded sequence.

In terms of compression, a DAC structure is very likely to outperform standard [base-128 compression schemes](https://en.wikipedia.org/wiki/Variable-length_quantity) aka VByte, Varint, VInt, EncInt etc..

As a bonus, a DAC structure gives to random access to each and every sequence element without any decoding.

## Installation
Install from PyPi using
```bash
pip install pyDAC
```

## Usage
```python
from pyDAC import DAC
```
imports the module.

```python
import random 
from pyDAC import DAC

values = random.sample(range(2**32), 10**7)
encoded_values = DAC(iter(values))
```
creates a DAC structure ``encoded_values`` for the ``values`` sequence. 

### Access
The ``i``th element from the original ``values`` sequence can be retrieved from a DAC structure ``encoded_values`` using the subscript operator
```python
for i in range(len(values)):
    assert values[i] == encoded_values[i]
```

A DAC structure ``encoded_values`` is also iterable. 

You can easily loop through the stored elements stored 
```python
dac_iter = iter(encoded_values)
while True:
    try:
        val = next(dac_iter)
    except StopIteration:
        break  # Iterator exhausted: stop the loop
    else:
        print(val)
```
or return all stored elements at once
```python
assert values == list(iter(encoded_values))
```


### Miscellaneous
A DAC structure can provide ``compression ratios`` and ``space_savings`` in comparision to the minimal fixed width representation and to the variable byte representation of the original ``values`` sequence. 

For example,
```python
values = [1, 2, 1, 8, 3, 4, 5, 9, 13, 1024, 262189]
encoded_values = DAC(iter(values))

print(encoded_values.space_savings)
>>> {'vbyte': 0.08214285714285718, 'fixed_width': 0.508133971291866}

print(encoded_values.compression_ratios)
>>> {'vbyte': 1.0894941634241246, 'fixed_width': 2.0330739299610894}
```

## Attributions

```bibtex
@article{
    title = {{Algorithms and Compressed Data Structures for Information Retrieval}},
    author = {Ladra, Susana},
    type = {Phd Thesis},
    institution = {Universidade da Coru{\~{n}}a},
    pages = {272},
    year = {2011},
    isbn = {5626895531}
}
```

```bibtex
@inproceedings{
    title = {{Directly addressable variable-length codes}},
    author = {Brisaboa, Nieves R. and Ladra, Susana and Navarro, Gonzalo},
    booktitle = {Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics)},
    volume = {5721 LNCS},
    doi = {10.1007/978-3-642-03784-9_12},
    isbn = {3642037836},
    issn = {03029743},
    pages = {122--130},
    publisher = {Springer, Berlin, Heidelberg},
    year = {2009}
}
```

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.