# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Plotting process functions."""
import pandas
import numpy as np

__all__ = ['generate_points']

type _Float2D = np.ndarray[
    tuple[int, int],
    np.dtype[np.float64]
]


def generate_points(
    df: pandas.DataFrame
) -> _Float2D:
    """Generates an NDArray of the points.

    Parameters
    ----------
    df : DataFrame
        The ``DataFrame`` of the data points.

    Returns
    -------
    points : NDArray in shape (n,2,)
        The array of points.

    Raises
    ------
    NotImplementedError
        The shape is not implemented in this version.
    """
    if df.shape[0] == 2:
        return df.T.to_numpy()
    elif df.shape[1] == 2:
        return df.to_numpy()
    raise NotImplementedError()
