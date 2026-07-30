"""Plotting module."""
import matplotlib.pyplot as plt
import numpy as np
import pandas
from typing import Any
from scipy.stats import linregress

__all__ = ['plot_dna']

type _Float1D = np.ndarray[
    tuple[int],
    np.dtype[np.floating[Any]]
]
type _Float2D = np.ndarray[
    tuple[int, int],
    np.dtype[np.floating[Any]]
]


def plot_dna(
    bdata: pandas.DataFrame,
    style: str = 'default'
) -> tuple[_Float1D, _Float1D]:
    """Plots the data from the ``DataFrame`` and returns the linear regression result.

    Parameters
    ----------
    bdata : DataFrame
        The ``DataFrame`` of the bands of DNA ladder.
    style : Valid MatplotLib style
        The plotting style.

    Returns
    -------
    coeffs : Array in shape (2,)
        The coefficients.
    err : Array in shape (2,)
        The standard errors.

    Notes
    -----
    The ``bdata`` parameter must be the following shape.

    +-------------+----------+
    | Length / bp | Location |
    +=============+==========+
    | 12345       | 89.07    |
    +-------------+----------+
    | ...         | ...      |
    +-------------+----------+
    """
    lengths: _Float1D = bdata.iloc[:, 0].to_numpy()
    locations: _Float1D = bdata.iloc[:, 1].to_numpy()
    regressR = linregress(locations, np.log10(lengths))
    plt.style.use(style)
    plt.semilogy(
        locations,
        lengths,
        '.'
    )
    plt.plot(
        locations,
        10 ** (regressR.slope * locations + regressR.intercept)
    )
    plt.xlabel('Locations')
    plt.ylabel('DNA length / bp')
    plt.grid()
    plt.grid(which='minor', color='0.8')
    plt.show()
    return np.array((regressR.slope, regressR.intercept)), np.array((regressR.stderr, regressR.intercept_stderr))
