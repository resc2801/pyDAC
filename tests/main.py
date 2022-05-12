import random
from typing import Tuple

import numpy as np
import tensorflow_probability as tfp

from pyDAC import DAC


def generate_values(n: int, bit_range: Tuple[int,int], tfp_distr , distr_params):
    """
    Helper function to generate unsigned ints within given bit_size_range from a distribution distr
    :param n:
    :param bit_range:
    :param distr:
    :param distr_params:
    :return:
    """

    distr_samples = tfp_distr(*distr_params).sample([n]).numpy()
    bit_sizes = np.round(bit_range[0] + (bit_range[1] - bit_range[0]) * distr_samples).astype(int).tolist()

    return [int((1 << (bit_size - 1)) | random.getrandbits(bit_size)) for bit_size in bit_sizes]


NUM_VALUES = 10 ** 5
MIN_BIT_SIZE = 3
MAX_BIT_SIZE = 64


####################################################################################################################
# Beta distribution on [0,1]
####################################################################################################################
alpha, beta = 2.0, 10.0
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Beta, (alpha, beta))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)

# special case for α = β and α, β → ∞: Normal distribution on [0,1]
# A beta(a, b) distribution is approximately normal if the parameters a and b are large and approximately equal.
# A beta(a,b) distribution has mean a/(a+b) and variance ab/(a+b)2(a+b+1).
# When a=b, this reduces to mean 1/2 and variance 1/(8a + 4).
alpha, beta = 10.0, 10.0
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Beta, (alpha, beta))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)

# special case for α = β = 1.0 Uniform distribution on [0,1]
alpha, beta = 1.0, 1.0
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Beta, (alpha, beta))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)

# special case # special case for α = β = 0.5: Arcsine distribution on [0,1]
alpha, beta = 0.5, 0.5
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Beta, (alpha, beta))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)


####################################################################################################################
# Uniform distribution on [0,1]
####################################################################################################################
params = (0.0, 1.0)  # low, high
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Uniform, params)

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)


####################################################################################################################
# Kumaraswamy distribution on [0,1]: similar to Beta distribution
####################################################################################################################
alpha, beta = 0.5, 0.5
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Kumaraswamy, (alpha, beta))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)


####################################################################################################################
# Bates distribution on [0,1]
####################################################################################################################
n, l, h = (3, 0.0, 1.0)  # total_count, low, high
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Bates, (n, l, h))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)

# special case for n → ∞: Gaussian distribution.
n, l, h = (20, 0.0, 1.0)  # total_count, low, high
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Bates, (n, l, h))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)

# special case: Triangular distribution
params = (2, 0.0, 1.0)  # total_count, low, high
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Bates, params)

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)

# special case: Uniform distribution
params = (1, 0.0, 1.0)  # total_count, low, high
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Bates, params)

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)


####################################################################################################################
# TriangularDistribution
####################################################################################################################
low, high, peak = (0.0, 1.0, 0.5)
values = generate_values(NUM_VALUES, (MIN_BIT_SIZE, MAX_BIT_SIZE), tfp.distributions.Triangular, (low, high, peak))

my_dac = DAC(iter(values))
print(my_dac.block_sizes, my_dac.bit_length, my_dac.compression_ratio)