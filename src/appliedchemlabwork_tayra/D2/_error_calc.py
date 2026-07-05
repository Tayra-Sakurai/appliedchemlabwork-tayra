# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import numpy as np
import pandas
from typing import Any, overload
import numpy.typing as npt


def calc_weighted_mean(
    data: pandas.DataFrame,
    absorbance: pandas.DataFrame
) -> pandas.DataFrame:
    """Calculates the weighted mean of the adsorption rate.

    Parameters
    ----------
    data : DataFrame
        The ``DataFrame`` which represents the data of original solution.
    absorbance : DataFrame
        The ``Dataframe`` which represents the data of experiment.

    Returns
    -------
    df : DataFrame
        The ``DataFrame`` of the calculated mean value by pH.

    Raises
    ------
    Exception
        The format of table is not suitable.

    Notes
    -----
    The suitable table format for ``absorbance`` is:

    +-----+--------------------------------------------+--------------------------------------+---------------------------+---------------------------+
    | pH  | :math:`A`, :math:`\\lambda_1`, Flow-through | :math:`A`, :math:`\\lambda_2`, Eluted | :math:`A,\\ \\lambda_2`, FT | :math:`A,\\ \\lambda_2`, El |
    +=====+============================================+======================================+===========================+===========================+
    | 6.5 | 0.118                                      | 0.033                                | 0.404                     | 0.015                     |
    +-----+--------------------------------------------+--------------------------------------+---------------------------+---------------------------+
    | 8.0 | 0.086                                      | 0.065                                | 0.285                     | 0.112                     |
    +-----+--------------------------------------------+--------------------------------------+---------------------------+---------------------------+

    One for ``data`` is:

    +-------------------+-------------------+
    | :math:`\\lambda_1` | :math:`\\lambda_2` |
    +===================+===================+
    | 0.461             | 0.093             |
    +-------------------+-------------------+
    """
    source = data.iloc[0].to_numpy()
    pH = absorbance.iloc[:, 0]
    df = pandas.DataFrame(data=pH)
    label = 'Adsorpted Rate'
    adata = absorbance.iloc[:, [1, 3]].to_numpy()
    weights = calc_weight(adata, source)
    ratio = adata / source
    ratio = 1 - ratio
    col, sum_of_weights = np.average(
        ratio,
        1,
        weights,
        returned=True
    )
    df[label] = col
    df['Errors'] = 1 / np.sqrt(sum_of_weights)
    return df



def calc_weight(
    absorbance_1: np.ndarray[
        tuple[int, int],
        np.dtype[np.floating[Any]]
    ],
    absorbance_2: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ]
) -> npt.NDArray[np.floating[Any]]:
    """Calculates the weight(s) from the absorbance data.

    Parameters
    ----------
    absorbance_1 : NDArray in shape (m, n)
        The absorbance of the first param.
    absorbance_2 : NDArray in shape (n,)
        The absorbance of the second item.

    Returns
    -------
    weights : NDArray in shape (m, n)
        The weight array.
    """
    ratio = (absorbance_2 / absorbance_1) ** 2
    ln10: np.float64 = np.emath.log(10)
    coeff = (1 / (ln10 * np.exp(ln10 * absorbance_1) * absorbance_1)) ** 2 + (1 / (ln10 * np.exp(ln10 * absorbance_2) * absorbance_2)) ** 2
    return ratio / (coeff ** 2)
