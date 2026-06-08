# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import QSlider
import numpy as np
from ._pattern_match import *
from typing import Any
import pandas
from ._calc_process import calc_k_from_data
__all__ = ['FindThread', 'AnalyzeThread']


class FindThread(QThread):
    stepped = pyqtSignal(int)
    ended = pyqtSignal(pandas.DataFrame)
    started = pyqtSignal(int)

    def __init__(
        self,
        parent: QObject,
        xmin: QSlider,
        xmax: QSlider,
        ymin: QSlider,
        ymax: QSlider,
        zmin: QSlider,
        zmax: QSlider,
        umin: QSlider,
        umax: QSlider
    ) -> None:
        super().__init__(parent)
        (
            self.xmin,
            self.xmax,
            self.ymin,
            self.ymax,
            self.zmin,
            self.zmax,
            self.umin,
            self.umax,
        ) = (
            xmin,
            xmax,
            ymin,
            ymax,
            zmin,
            zmax,
            umin,
            umax,
        )

    def run(self) -> None:
        xrange = np.arange(self.xmin.value(), self.xmax.value(), 5)
        yrange = np.arange(self.ymin.value(), self.ymax.value(), 5)
        zrange = np.arange(self.zmin.value(), self.zmax.value(), 5)
        urange = np.arange(self.umin.value(), self.umax.value(), 5)
        size = np.prod((xrange.size, yrange.size, zrange.size, urange.size))
        self.started.emit(int(size))
        i: int = 0
        results: list[
            tuple[
                np.integer[Any],
                np.integer[Any],
                np.integer[Any],
                np.integer[Any],
                np.float64
            ]
        ] = []
        for x in xrange:
            for y in yrange:
                for z in zrange:
                    for u in urange:
                        i += 1
                        self.stepped.emit(i)
                        xl = x / 1000
                        yl = y / 1000
                        zl = z / 1000
                        ul = u / 1000
                        c, th = check_match(xl, yl, zl, ul)
                        print(c, i, size)
                        if c:
                            results.append((
                                x,
                                y,
                                z,
                                u,
                                th
                            ))
        rarray = np.array(results, dtype=np.float64)
        self.ended.emit(
            pandas.DataFrame(
                data=rarray,
                columns=(
                    '酢エチに加える水の体積 / mL',
                    '6 M NaOH に加える水の体積 / mL',
                    '反応液に加える水量 / mL',
                    '反応液に加える NaOH 希釈液の体積 / mL',
                    '半減期 (274 K) / s',
                )
            )
        )

class AnalyzeThread(QThread):
    ended = pyqtSignal(pandas.DataFrame)

    def __init__(
        self,
        v_t_and_t: pandas.DataFrame,
        v_hcl: float,
        v_r: float,
        c_base: float,
        c_hcl: float,
        a: float,
        b: float,
        k_pred: float,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        (
            self.v_t_and_t,
            self.v_hcl,
            self.v_r,
            self.c_base,
            self.c_hcl,
            self.a,
            self.b,
            self.k_pred,
        ) = (
            v_t_and_t,
            v_hcl,
            v_r,
            c_base,
            c_hcl,
            a,
            b,
            k_pred,
        )

    def run(self) -> None:
        df = calc_k_from_data(self.k_pred, self.v_r, self.v_hcl, self.c_base, self.c_hcl, self.a, self.b, self.v_t_and_t)
        self.ended.emit(df)
