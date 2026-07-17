# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import pandas
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QVBoxLayout
from PyQt6.QtGraphs import QScatterSeries, QGraphsLine, QLineSeries, QLegendData, QGraphsTheme, QValueAxis
from os import PathLike
from typing import TextIO, Any
from PyQt6.QtCore import QObject


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
