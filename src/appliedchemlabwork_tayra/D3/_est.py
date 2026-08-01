# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import pandas
import numpy as np
from typing import Any

__all__ = ['estimate']

type _Float1D = np.ndarray[
    tuple[int],
    np.dtype[np.float64]
]


def estimate(
    slope: np.floating[Any] | float,
    intercept: np.floating[Any] | float,
    df: pandas.DataFrame
) -> pandas.DataFrame:
    """Estimates the length of the DNA from the line data.

    Parameters
    ----------
    slope : floating number
        The slope of the line.
    intercept : floating number
        The intercept of the line.
    df : DataFrame
        The table data.

    Returns
    -------
    df : DataFrame
        Modified DataFrame object.
    """
    y: _Float1D = df.iloc[:, 0].to_numpy()
    x = (y - intercept) / slope
    col_name = 'Estimated length of DNA / bp'
    count = 0
    while col_name in df.columns:
        count += 1
        col_name = f'Estimated length of DNA ({count}) / bp'
    df[col_name] = x
    return df
