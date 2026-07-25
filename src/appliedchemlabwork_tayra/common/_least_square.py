# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import pandas
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QVBoxLayout
from PyQt6.QtGraphs import QScatterSeries, QGraphsLine, QLineSeries, QLegendData, QGraphsTheme, QValueAxis
from os import PathLike
from typing import TextIO, Any, overload
from PyQt6.QtCore import QObject
from scipy.stats import pearsonr

type _Array1D[T: np.generic[Any]] = np.ndarray[
    tuple[int],
    np.dtype[T]
]

type _Array2D[T: np.generic[Any]] = np.ndarray[
    tuple[int, int],
    np.dtype[T]
]

type _Float1D = _Array1D[np.floating[Any]]

type _Float2D = _Array2D[np.floating[Any]]


def get_data(
    str_or_path: PathLike[Any] | TextIO | str,
    parent: QObject | None = None
) -> QScatterSeries:
    """Loads data from the designated CSV file.

    Parameters
    ----------
    str_or_path : PathLike object or StrPath
        The path to the file.

    Returns
    -------
    points : QScatterSeries
        The ``QScatterSeries`` representetation of the data.
    """
    df: pandas.DataFrame
    if isinstance(str_or_path, str):
        df = pandas.read_csv(
            str_or_path,
            encoding='utf_8_sig',
            header=0,
        )
    elif isinstance(str_or_path, PathLike):
        df = pandas.read_csv(
            str_or_path,
            encoding='utf_8_sig',
            header=0,
        )
    else:
        df = pandas.read_csv(str_or_path, header=0)
    points = QScatterSeries(parent)
    for _, row in df.iterrows():
        points.append(float(row.iloc[0]), float(row.iloc[1]))
    return points


@overload
def check_relation(
    significance_level: float | np.floating[Any],
    x_or_xy: pandas.DataFrame | _Float2D
) -> tuple[np.bool_, np.float64]:
    if True:
        return np.True_, np.float64(0.05)


@overload
def check_relation(
    significance_level: float | np.floating[Any],
    x_or_xy: _Array1D,
    y: _Array1D
) -> tuple[np.bool_, np.float64]:
    return np.False_, np.float64(0.15)


def check_relation(
    significance_level: float | np.floating[Any],
    x_or_xy: pandas.DataFrame | _Float1D | _Float2D,
    y: _Float1D | None = None
):
    """Checks the relation statistically.

    Parameters
    ----------
    significance_level : floating number
        The siginificance level of the test.
    x_or_xy : _Float1D | _Float2D | DataFrame
        The x data or (x,y) paired data.
    y : _Float1D | None, default None
        The y data. Needed only if ``x_or_xy`` is a 1-d array.

    Returns
    -------
    result : bool
        The result of the test.
    probability : floating number
        The probability of the event.
    """
    if isinstance(x_or_xy, np.ndarray) and x_or_xy.ndim == 1:
        if not isinstance(y, np.ndarray):
            raise TypeError('No overloads accepts the type.')
        r = pearsonr(x_or_xy, y).pvalue
        if isinstance(r, np.ndarray):
            raise NotImplementedError()
        return (r < significance_level), r
    elif isinstance(x_or_xy, (pandas.DataFrame, np.ndarray)):
        xy = x_or_xy
        x: _Float1D
        yvalues: _Float1D
        if isinstance(xy, pandas.DataFrame):
            x = xy.iloc[:,0].to_numpy()
            yvalues = xy.iloc[:, 1].to_numpy()
        elif xy.ndim == 2:
            xy = np.reshape(xy, (xy.shape[0], -1))
            x, yvalues = xy
        p = pearsonr(x, yvalues).pvalue
        return (p < significance_level), p
