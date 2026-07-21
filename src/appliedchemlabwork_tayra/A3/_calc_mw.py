"""Calculates the molecular weight by using Mark-Houwink-Sakurada's equation."""
import numpy as np
from scipy.optimize import lsq_linear
from typing import Any

__all__ = ['calc_intrisic_viscosity', 'calc_mw']

type _Array1D = np.ndarray[
    tuple[int],
    np.dtype[np.floating[Any]]
]


def calc_intrisic_viscosity[
    Shape: tuple[int]
](
    concentration: np.ndarray[
        Shape,
        np.dtype[np.floating[Any]]
    ],
    reduced: np.ndarray[
        Shape,
        np.dtype[np.floating[Any]]
    ],
    inherent: np.ndarray[
        Shape,
        np.dtype[np.floating[Any]]
    ]
) -> _Array1D:
    """Calculates the intrisic viscosity with double extrapolation.

    Parameters
    ----------
    concentration : Array in shape (m,)
        The concentration array.
    reduced : Array in shape (m,)
        The reduced viscosities.
    inherent : Array in shape (m,)
        The inherent viscosities.

    Returns
    -------
    viscosity_and_coeffs : Array in shape (3,)
        The intrisic viscosity, Huggins' coefficient, and Kraemer's formula.
    """
    indeps = np.ones(concentration.shape)
    spaces = np.zeros(concentration.shape)
    upper = np.column_stack((indeps, concentration, spaces,))
    lower = np.column_stack((indeps, spaces, concentration,))
    a = np.concat((upper, lower), axis=0)
    print('A =', a)
    b = np.append(reduced, inherent)
    print('b =', b)
    res = lsq_linear(a, b)
    return res.x


def calc_mw(
    intrisic_viscosity: float | np.floating[Any],
    K: float | np.floating[Any],
    alpha: float | np.floating[Any]
) -> np.float64:
    """Calculates the molecular weight.

    Parameters
    ----------
    intrisic_viscosity : floating[Any]
        The intrisic viscosity.
    K : floating[Any]
        The :math:`K` value for Mark-Houwink-Sakurada's formula.
    alpha : floating[Any]
        The :math:`\\alpha` value for Mark-Houwink-Sakurada's formula.

    Returns
    -------
    mw : float64
        The molecular weight.

    Notes
    -----
    Mark-Houwink-Sakurada's formula is defined as:

    .. math::

       \\left[ \\eta \\right] ={} K M^{\\alpha}
    """
    res = (intrisic_viscosity / K) ** (1 / alpha)
    return np.float64(res)
