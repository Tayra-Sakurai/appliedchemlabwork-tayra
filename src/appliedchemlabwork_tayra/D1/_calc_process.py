# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""The process calculators."""
from scipy.optimize import curve_fit
import numpy as np
from typing import Any, overload
import pandas

__all__ = ['calc_k_from_data']


@overload
def calc_k_from_data(
    k_pred: float | np.floating[Any],
    v_r: float | np.floating[Any],
    v_hcl: float | np.floating[Any],
    c_base: float | np.floating[Any],
    c_hcl: float | np.floating[Any],
    a: float | np.floating[Any],
    b: float | np.floating[Any],
    vt_or_table: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ],
    v_t_inf: float | np.floating[Any],
    t: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ]
) -> pandas.DataFrame:
    return pandas.DataFrame()


@overload
def calc_k_from_data(
    k_pred: float | np.floating[Any],
    v_r: float | np.floating[Any],
    v_hcl: float | np.floating[Any],
    c_base: float | np.floating[Any],
    c_hcl: float | np.floating[Any],
    a: float | np.floating[Any],
    b: float | np.floating[Any],
    vt_or_table: pandas.DataFrame,
    v_t_inf: float | np.floating[Any]
) -> pandas.DataFrame:
    return pandas.DataFrame()


def calc_k_from_data(
    k_pred: float | np.floating[Any],
    v_r: float | np.floating[Any],
    v_hcl: float | np.floating[Any],
    c_base: float | np.floating[Any],
    c_hcl: float | np.floating[Any],
    a: float | np.floating[Any],
    b: float | np.floating[Any],
    vt_or_table: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ] |
    pandas.DataFrame,
    v_t_inf: float | np.floating[Any],
    t: np.ndarray[
        tuple[int],
        np.dtype[np.number[Any, int | float]]
    ] | None = None
):
    """Calculates the ``k`` value.

    Parameters
    ----------
    k_pred : floating[Any]
        The predicted reaction pace coefficient.
    v_r : floating[Any]
        The collected volume of the reaction solution.
    v_hcl : floating[Any]
        The added volume of the HCl aq.
    c_base : floating[Any]
        The concentration of titrating base.
    c_hcl : floating[Any]
        The concentration of HCl used to stop the reaction.
    a : floating number
        The initial concentration (in molarity)
        of AcOEt in the reaction solution.
    b : floating number
        The initial concentration of the base in the 
        reaction solution.
    vt_or_table : DataFrame or NDArray in shape (n,)
        The table of time and titrated volume of the base,
        or an ``NDArray`` which represents the titrated volume
        of the base.
    v_t_inf : floating value
        The titrated volume at the time of :math:`t ={} \\infty`.

    Other Parameters
    ----------------
    t : NDArray in shape (n,)
        Necessary when you have given ``vt_or_table`` an ``NDArray``.
        The times when you collected the sample.

    Returns
    -------
    df : DataFrame
        The table of values and errors.

    Raises
    ------
    TypeError
        The parameters' types are not valid.

    Notes
    -----
    When ``vt_or_table`` was given as a ``DataFrame``,
    the table style must be like:

    +-----------+-------+-------+
    |   t / s   |   76  |  ...  |
    +-----------+-------+-------+
    | Vt / cm^3 | 18.82 |  ...  |
    +-----------+-------+-------+

    The ``vt_or_table`` and ``t`` must not include the infinite time data.
    """
    times: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ]
    vts: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ]
    if isinstance(vt_or_table, pandas.DataFrame):
        print(vt_or_table)
        timeSeries: pandas.Series[np.dtype[np.floating[Any]]] = vt_or_table.iloc[0]
        times = timeSeries.to_numpy()
        vts = vt_or_table.iloc[1].to_numpy()
    if isinstance(vt_or_table, np.ndarray) and isinstance(t, np.ndarray):
        times = t.view(np.dtype(np.float64))
        vts = vt_or_table
    amx: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ] = ((vts - v_t_inf) * c_base) / (-2 * v_r)
    bk = (b - a) * k_pred
    result, popt = curve_fit(
        _model,
        times,
        amx,
        p0=(
            a,
            b,
            bk,
        )
    )
    df = pandas.DataFrame(
        data={
            'Coefficients': result,
            'Errors': np.sqrt(np.diag(popt)),
        }
    )
    return df


def _model(
    x: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ],
    a: np.floating[Any] | float,
    b: np.floating[Any] | float,
    bk: np.floating[Any] | float
) -> np.ndarray[
    tuple[int],
    np.dtype[np.floating[Any]]
]:
    return a - (((a * b)*(np.exp(bk * x) - 1)) / (b * np.exp(bk * x) - a))
