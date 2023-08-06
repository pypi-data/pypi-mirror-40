"""Specific hypothesis strategies that are useful for testing.

It defines the following strategies:

- :code:`dimension`: Represents a size or dimension e.g. for numpy arrays image
  sizes etc.
- :code:`real`: Represents a real number in the range +/-1 million
"""
import numpy as np
from math import pi

from stylo.error import MissingDependencyError

try:
    from hypothesis.strategies import integers, floats, tuples
    from hypothesis.extra.numpy import arrays

except ImportError as err:
    raise MissingDependencyError(
        "The testing package requires additional dependencies."
        " Run `pip install stylo[testing]` to install them."
    ) from err

# Basic types
real = floats(min_value=-1e6, max_value=1e6)
angle = floats(min_value=-pi, max_value=pi)
dimension = integers(min_value=4, max_value=1024)
small_dimension = integers(min_value=4, max_value=128)
image_size = tuples(small_dimension, small_dimension)

# Stylo data
domain_values = arrays(np.float64, image_size, elements=real)
shape_mask = arrays(np.bool_, image_size)
