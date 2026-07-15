# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import pandas
import numpy as np
import numpy.typing as npt
from typing import Any

__all__ = ["calc_concentration"]

type _DataArray2D = np.ndarray[
    tuple[int, int],
    np.dtype[np.floating[Any]]
]
type _DataArray1D = np.ndarray[
    tuple[int],
    np.dtype[np.floating[Any]]
]
type _Array1D[T: np.number[Any, Any]] = np.ndarray[
    tuple[int],
    np.dtype[T]
]


def calc_concentration(
    data: pandas.DataFrame,
    epsilon: pandas.DataFrame,
    l: float | np.floating[Any] = 1.0e-2
) -> pandas.DataFrame:
    """Calculates the concentration of the molarity of the solutions.

    Parameters
    ----------
    data : DataFrame
        The ``DataFrame`` of the absorbances.
    epsilon : DataFrame
        The ``DataFrame`` of the absorption coefficients by wavelength.
    l : floating number, default to 1.0e-2
        The optical path length of the optical cell in metre.

    Returns
    -------
    df : DataFrame
        The result table data.

    Notes
    -----
    This function's parameters are templeted in the following styles.

    ``data`` Style
    ^^^^^^^^^^^^^^
    +--------+--------------------------------------------+--------------------------------------+---------------------------+---------------------------+
    | Sample | :math:`A`, :math:`\\lambda_1`, Flow-through | :math:`A`, :math:`\\lambda_2`, Eluted | :math:`A,\\ \\lambda_2`, FT | :math:`A,\\ \\lambda_2`, El |
    +========+============================================+======================================+===========================+===========================+
    | 1      | 0.118                                      | 0.033                                | 0.404                     | 0.015                     |
    +--------+--------------------------------------------+--------------------------------------+---------------------------+---------------------------+
    | 2      | 0.086                                      | 0.065                                | 0.285                     | 0.112                     |
    +--------+--------------------------------------------+--------------------------------------+---------------------------+---------------------------+

    ``epsilon`` Data Style
    ^^^^^^^^^^^^^^^^^^^^^^
    +-------------------+-------------------+
    | :math:`\\lambda_1` | :math:`\\lambda_2` |
    +===================+===================+
    | 2.63e9            | 1.30e10           |
    +-------------------+-------------------+

    ``df`` Data Style
    ^^^^^^^^^^^^^^^^^
    +---------------------------+---------------------+
    | Flow-through / mol L^(-1) | Eluted / mol L^(-1) |
    +===========================+=====================+
    | 2.39e-9                   | 5.49e-9             |
    +---------------------------+---------------------+

    About the Concentration
    ^^^^^^^^^^^^^^^^^^^^^^^
    The molarity is calculated by using Lambert-Beer law.
    According to the law, the molarity and the absorbance
    is represented in the following equation:

    .. math::

       A ={} \\varepsilon c l

    This equation shows that the absorbance is proportional to molarity.
    """
    absorbances_ft: _DataArray2D = data.iloc[:, [0, 2]].to_numpy()
    absorbances_el: _DataArray2D = data.iloc[:, [1, 3]].to_numpy()
    epsilons: _DataArray2D = epsilon.to_numpy()
    les: _DataArray2D = epsilons * l
    left: _DataArray2D = les.T
    r1: _DataArray1D = absorbances_ft.T.flatten()
    r2: _DataArray1D = absorbances_el.T.flatten()
    results1: _Array1D[np.float32] = np.linalg.solve(left, r1)
    results2: _Array1D[np.float32] = np.linalg.solve(left, r2)
    df = pandas.DataFrame(
        data={
            'Flow-through': results1,
            'Eluted': results2,
        }
    )
    return df
