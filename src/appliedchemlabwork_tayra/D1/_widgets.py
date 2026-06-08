# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QMainWindow, QPushButton, QFileDialog, QGroupBox, QVBoxLayout, QSlider, QProgressDialog
import os
import pandas
from ._threads import *

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
        sLayout = QVBoxLayout(self)

        g1 = QGroupBox(self)
        g1Layout = QFormLayout(g1)
        g1.setTitle('予習用ツール')
        self.dataFilePathInput = QLineEdit(g1)
        dataFileLabel = QLabel('Data File Path', g1)
        g1Layout.addRow(dataFileLabel, self.dataFilePathInput)
        self.p1 = QPushButton('Or pick a CSV file.', g1)
        self.p1.clicked.connect(self._fpick(self.dataFilePathInput))
        p1Label = QLabel('Or', g1)
        g1Layout.addRow(p1Label, self.p1)

        doubleValidation = QDoubleValidator(-2048., 2047., 3)

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

        sLayout.insertWidget(0, g1)

        g2 = QGroupBox(self)
        g2Layout = QFormLayout(g2)

        self.k_pred_input = QLineEdit(g2)
        self.k_pred_input.setValidator(doubleValidation)
        k_pred_label = QLabel('k の予想値', g2)
        g2Layout.addRow(k_pred_label, self.k_pred_input)

        self.a_input = QLineEdit(g2)
        self.a_input.setValidator(doubleValidation)
        a_label = QLabel('a の予測値 / M', g2)
        g2Layout.addRow(a_label, self.a_input)

        self.b_input = QLineEdit(g2)
        self.b_input.setValidator(doubleValidation)
        b_label = QLabel('b の予測値 / M', g2)
        g2Layout.addRow(b_label, self.b_input)

        self.c_hcl_input = QLineEdit(g2)
        self.c_hcl_input.setValidator(doubleValidation)
        c_hcl_label = QLabel('塩酸のモル濃度 / M', g2)
        g2Layout.addRow(c_hcl_label, self.c_hcl_input)

        self.c_base_input = QLineEdit(g2)
        self.c_base_input.setValidator(doubleValidation)
        c_base_label = QLabel('滴定に用いた塩基の濃度 / M')
        g2Layout.addRow(c_base_label, self.c_base_input)

        self.v_r_input = QLineEdit(g2)
        self.v_r_input.setValidator(doubleValidation)
        v_r_label = QLabel('反応液の分取量 / mL', g2)
        g2Layout.addRow(v_r_label, self.v_r_input)

        self.v_hcl_input = QLineEdit(g2)
        self.v_hcl_input.setValidator(doubleValidation)
        v_hcl_label = QLabel('塩酸の滴下量 / mL', g2)
        g2Layout.addRow(v_hcl_label, self.v_hcl_input)

        self.v_t_t_path_input = QLineEdit(g2)
        v_t_t_path_label = QLabel('滴下量と時刻のデータファイル', g2)
        g2Layout.addRow(v_t_t_path_label, self.v_t_t_path_input)

        choose_btn = QPushButton('ファイルを選択', g2)
        choose_btn.clicked.connect(self._fpick(self.v_t_t_path_input))
        choose_label = QLabel('または', g2)
        g2Layout.addRow(choose_label, choose_btn)

        submit2 = QPushButton('送信', g2)
        submit2.clicked.connect(self._analyze)
        sl2 = QLabel('送信する', g2)
        g2Layout.addRow(sl2, submit2)

        g2.setTitle('結果の解析ツール')

        sLayout.insertWidget(1, g2)

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
        self.qThread.stepped.connect(self._progressStep)
        self.qThread.ended.connect(self._save_data)

    def _file_pick(self, i: QLineEdit):
        fName, _ = QFileDialog.getOpenFileName(
            self,
            'CSV ファイルを選択',
            os.curdir,
            'CSV ファイル コンマ区切り UTF-8 (*.csv)'
        )
        i.setText(fName)

    def _fpick(self, i: QLineEdit):
        return lambda: self._file_pick(i)
    
    def _predict(self):
        self.progress.show()
        self.qThread.start()

    def _progressSet(
        self,
        arg: int
    ):
        self.progress.setMaximum(arg)

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

    def _analyze(self):
        aThread = AnalyzeThread(
            pandas.read_csv(
                self.v_t_t_path_input.text(),
                encoding='utf_8_sig'
            ),
            float(self.v_hcl_input.text()),
            float(self.v_r_input.text()),
            float(self.c_base_input.text()),
            float(self.c_hcl_input.text()),
            float(self.a_input.text()),
            float(self.b_input.text()),
            float(self.k_pred_input.text()),
            self
        )
        aThread.ended.connect(self._save_data)
        aThread.start()
