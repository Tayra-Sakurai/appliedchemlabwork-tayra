# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""The process calculators."""
from scipy.optimize import least_squares
import numpy as np
from typing import Any, overload
import pandas
import numpy.typing as npt

__all__ = ['calc_k_from_data', 'calc_left']


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
    vt_or_table: pandas.DataFrame
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
    """
    if (
        isinstance(vt_or_table, np.ndarray) and
        isinstance(t, np.ndarray)
    ):
        result = least_squares(
            _calc_residual,
            np.array(
                (
                    k_pred,
                    a,
                    b,
                )
            ),
            args=(
                vt_or_table,
                t,
                v_r,
                v_hcl,
                c_hcl,
                c_base,
            )
        )
        f = result.fun
        j = np.array(result.jac)
        dof = len(f) - len(result.x)
        rss = np.sum(f ** 2)
        mse = rss / dof
        cov_matrix = np.linalg.inv(np.dot(j.T, j)) * mse
        stderr = np.sqrt(np.diag(cov_matrix))
        df = pandas.DataFrame(
            data=[
                result.x,
                stderr
            ],
            columns=('Value', 'Error'),
            index=('k', 'a', 'b',)
        )
        return df
    elif isinstance(vt_or_table, pandas.DataFrame):
        vt: pandas.Series[np.dtype[np.floating[Any]]] = vt_or_table.iloc[1]
        time: pandas.Series[np.dtype[np.floating[Any]]] = vt_or_table.iloc[0]
        result = least_squares(
            _calc_residual,
            np.array(
                (
                    k_pred,
                    a,
                    b,
                )
            ),
            args=(
                vt.to_numpy(),
                time.to_numpy(),
                v_r,
                v_hcl,
                c_hcl,
                c_base,
            )
        )
        f = result.fun
        j = np.array(result.jac)
        dof = len(f) - len(result.x)
        rss = np.sum(f ** 2)
        mse = rss / dof
        cov_matrix = np.linalg.inv(np.dot(j.T, j)) * mse
        stderr = np.sqrt(np.diag(cov_matrix))
        df = pandas.DataFrame(
            data=[
                result.x,
                stderr
            ],
            columns=('Value', 'Error'),
            index=('k', 'a', 'b',)
        )
        return df


def calc_left(
    x: npt.NDArray[np.floating[Any]],
    a: float | np.floating[Any],
    b: float | np.floating[Any]
) -> npt.NDArray[np.floating[Any]]:
    """Calculates the value which is proprtional to ``k`` and ``t``.

    Parameters
    ----------
    x : NDArray[floating[Any]]
        The reduced concentration of the reactant.
    a : floating[Any]
        The initial concentration of the reactant ester.
    b : floating[Any]
        The initial concentration of the base.

    Returns
    -------
    val : NDArray[floating[Any]]
        The value of the formula.

    Notes
    -----
    The value :math:`v` is equivalent to
    
    .. math:: v ={} \\ln \\frac{a \\left( b -{} x \\right)}{b \\left( a -{} x \\right)}
    """
    up = a * (b - x)
    den = b * (a - x)
    return np.log(up / den)


def _model(
    v_hcl: float | np.floating[Any],
    v_t: npt.NDArray[np.floating[Any]],
    c_base: float | np.floating[Any],
    c_hcl: float | np.floating[Any],
    v_r: float | np.floating[Any],
    a: float | np.floating[Any],
    b: float | np.floating[Any]
) -> npt.NDArray[np.floating[Any]]:
    x = (v_t * c_base - v_hcl * c_hcl + v_r * b) / (2 * v_r)
    return calc_left(x, a, b)


def _calc_residual[
    Shape: (
        tuple[int],
        tuple[int, int],
        tuple[int, int, int],
        tuple[int, ...]
    )
](
    parameters: np.ndarray[
        tuple[int],
        np.dtype[np.floating[Any]]
    ],
    v_t: np.ndarray[
        Shape,
        np.dtype[np.floating[Any]]
    ],
    t: np.ndarray[
        Shape,
        np.dtype[np.floating[Any]]
    ],
    v_r: float | np.floating[Any],
    v_hcl: float | np.floating[Any],
    c_hcl: float | np.floating[Any],
    c_base: float | np.floating[Any]
) -> np.floating[Any]:
    k, a, b = parameters
    residual = k * t - _model(
        v_hcl,
        v_t,
        c_base,
        c_hcl,
        v_r,
        a,
        b
    )
    return np.sqrt(np.sum(residual ** 2))
