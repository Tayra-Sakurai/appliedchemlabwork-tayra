# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QMainWindow, QPushButton, QFileDialog, QGroupBox, QStackedLayout, QSlider, QProgressDialog
import os
import numpy as np
from typing import Any
import pandas
from ._threads import FindThread

__all__ = ['_MainWindow']


class _MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowType = Qt.WindowType.Window) -> None:
        super().__init__(parent, flags)
        self.setWindowTitle('D1 酢酸エチルの加水分解')
        self.setGeometry(20, 10, 800, 500)

        self.mainWidget = _MainWidget(self)
        self.setCentralWidget(self.mainWidget)


class _MainWidget(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super().__init__(parent, flags)
        sLayout = QStackedLayout(self)

        g1 = QGroupBox(self)
        g1Layout = QFormLayout(g1)
        g1.setTitle('予習用ツール')
        self.dataFilePathInput = QLineEdit(g1)
        dataFileLabel = QLabel('Data File Path', g1)
        g1Layout.addRow(self.dataFilePathInput, dataFileLabel)
        self.p1 = QPushButton('Or pick a CSV file.', g1)
        self.p1.clicked.connect(self._fpick(self.dataFilePathInput))
        p1Label = QLabel('Or', g1)
        g1Layout.addRow(p1Label, self.p1)

        self.test_min_slider = QSlider(Qt.Orientation.Horizontal, g1)
        self.test_max_slider = QSlider(Qt.Orientation.Horizontal, g1)
        for slider in self.test_min_slider, self.test_max_slider:
            slider.setMinimum(600)
            slider.setMaximum(1100)
            slider.setTickInterval(10)
        self.test_max_slider.setValue(1000)
        self.test_min_slider.setValue(700)
        test_min_label = QLabel('NaOH に加える水の体積 - 最小値', g1)
        test_max_label = QLabel('NaOH に加える水の体積 - 最大値', g1)
        self.test_water_min_slider = QSlider(Qt.Orientation.Horizontal, g1)
        self.test_water_max_slider = QSlider(Qt.Orientation.Horizontal, g1)
        for slider in self.test_water_min_slider, self.test_water_max_slider:
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setTickInterval(10)
        self.test_water_max_slider.setValue(50)
        self.test_water_min_slider.setValue(50)
        test_water_min_label = QLabel('酢エチに加える水の体積 - 最小', g1)
        test_water_max_label = QLabel('酢エチに加える水の体積 - 最大', g1)
        self.test_r_water_min_slider = QSlider(Qt.Orientation.Horizontal, g1)
        self.test_r_water_max_slider = QSlider(Qt.Orientation.Horizontal, g1)
        for slider in self.test_r_water_max_slider, self.test_r_water_min_slider:
            slider.setMaximum(200)
            slider.setMinimum(50)
            slider.setTickInterval(5)
            slider.setValue(125)
        test_r_water_max_label = QLabel('反応液に加える水量 - 最大値', g1)
        test_r_water_min_label = QLabel('反応液に加える水量 - 最小値', g1)
        self.test_r_naoh_min_slider = QSlider(Qt.Orientation.Horizontal, g1)
        self.test_r_naoh_max_slider = QSlider(Qt.Orientation.Horizontal, g1)
        for slider in self.test_r_naoh_max_slider, self.test_r_naoh_min_slider:
            slider.setMinimum(75)
            slider.setMaximum(200)
            slider.setTickInterval(5)
        self.test_r_naoh_max_slider.setValue(75)
        self.test_r_naoh_min_slider.setValue(200)
        test_r_naoh_max_label = QLabel('NaOH の体積 - 反応 - 最大', g1)
        test_r_naoh_min_label = QLabel('NaOH の体積 - 反応 - 最小', g1)

        g1Layout.addRow(test_min_label, self.test_min_slider)
        g1Layout.addRow(test_max_label, self.test_max_slider)
        g1Layout.addRow(test_water_min_label, self.test_water_min_slider)
        g1Layout.addRow(test_water_max_label, self.test_water_max_slider)
        g1Layout.addRow(test_r_water_min_label, self.test_r_water_min_slider)
        g1Layout.addRow(test_r_water_max_label, self.test_r_water_max_slider)
        g1Layout.addRow(test_r_naoh_min_label, self.test_r_naoh_min_slider)
        g1Layout.addRow(test_r_naoh_max_label, self.test_r_naoh_max_slider)

        self.submit_btn = QPushButton('送信', g1)
        submit_btn_label = QLabel('送信', g1)
        self.submit_btn.clicked.connect(self._predict)
        g1Layout.addRow(submit_btn_label, self.submit_btn)

        sLayout.addWidget(g1)

        self.superBtn = QPushButton('結果を計算する', self)
        sLayout.addWidget(self.superBtn)

        self.progress = QProgressDialog(
            'Process...',
            'Cancel',
            0,
            100,
            self
        )
        self.progress.setAutoClose(True)
        self.progress.setAutoReset(True)

        self.qThread = FindThread(
            self,
            self.test_water_min_slider,
            self.test_water_max_slider,
            self.test_min_slider,
            self.test_max_slider,
            self.test_r_water_min_slider,
            self.test_r_water_max_slider,
            self.test_r_naoh_min_slider,
            self.test_r_naoh_max_slider
        )

        self.qThread.started.connect(
            self._progressSet
        )

    def _file_pick(self, i: QLineEdit):
        fName, _ = QFileDialog.getOpenFileName(
            self,
            'CSV ファイルを選択',
            os.curdir,
            'CSV ファイル コンマ区切り UTF-8 (*.csv)'
        )
        i.setText(fName)

    def _fpick(self, i: QLineEdit):
        def _func():
            return self._file_pick(i)
        return _func
    
    def _predict(self):
        self.progress.show()
        self.qThread.start()

    def _progressSet(
        self,
        arg: np.integer[Any]
    ):
        self.progress.setMaximum(int(arg))

    def _progressStep(
        self,
        i: int
    ):
        self.progress.setValue(i)

    def _save_data(
        self,
        df: pandas.DataFrame
    ):
        fName, _ = QFileDialog.getSaveFileName(
            self,
            'Save as...',
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),
            'CSV, UTF-8 (*.csv)',
            'CSV, UTF-8 (*.csv)'
        )
        df.to_csv(
            fName,
            encoding='utf_8_sig'
        )
