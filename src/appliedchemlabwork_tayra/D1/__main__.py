# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from typing import Any
import numpy as np
from ._pattern_match import check_match
import random
import argparse
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QWidget, QLabel, QLineEdit, QFormLayout, QPushButton, QApplication
from PyQt6.QtCore import QDir
from ._calc_data import *
import pandas
import sys


class CWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        
        layout = QFormLayout()
        self.filepathInput = QLineEdit(self)
        self.filepathInput.setReadOnly(True)
        label = QLabel("CSV File path", self)
        layout.addRow(label, self.filepathInput)
        btn = QPushButton('Submit', self)
        selectionBtn = QPushButton('Select CSV file.', self)
        selectionBtn.clicked.connect(
            lambda: self.filepathInput.setText(self.show_dialog())
        )

        layout.addRow(btn, selectionBtn)
        self.setLayout(layout)

    def show_dialog(self):
        fileDialog = QFileDialog(
            self,
            filter="CSV Files (*.csv *.txt)"
        )
        fileDialog.setViewMode(QFileDialog.ViewMode.Detail)
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileDialog.setWindowTitle('Please select a CSV file.')
        fileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        fileDialog.setAcceptDrops(True)
        fileDialog.setDefaultSuffix('.csv')
        fileDialog.setDirectory(QDir.home())
        if fileDialog.exec():
            return fileDialog.selectedFiles()[0]
        return ''
    
    def process_submit(self):
        df = pandas.read_csv(self.filepathInput.text(), encoding='utf_8_sig')
        data = calc_k_and_a(df)
        df2 = pandas.DataFrame(data, columns=('k', 'a'))
        self.save_to_file(df2)

    def save_to_file(self, df: pandas.DataFrame):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            'Save file.',
            QDir.homePath(),
            'CSV File (*.csv)'
        )
        df.to_csv(
            filepath,
            encoding='utf_8_sig'
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)
        self.setCentralWidget(CWidget(self))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--optimize',
        help='Optimizes for minimumn experiment time.',
        action='store_true'
    )
    args = parser.parse_args()
    try:
        v2s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(700e-3, 1., 1e-2)
        v1s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(10e-3, 2., 1e-2)
        v3s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(0, 2.5e-1, 1e-2)
        v4s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(100e-3, 240e-3, 1e-3)
        l: int = len(v1s) * len(v2s) * len(v3s) * len(v4s)
        plist: list[
            tuple[
                np.float64,
                np.ndarray[tuple[int], np.dtype[Any]]
            ]
        ] = []
        bksps: str = ''
        cnt: int = 0
        for v1 in v1s.flat:
            for v2 in v2s.flat:
                for v3 in v3s.flat:
                    for v4 in v4s.flat:
                        cnt += 1
                        message: str = f'{cnt} / {l}'
                        print(bksps, end='')
                        print(message, end='')
                        bksps = '\b' * len(message)
                        matching, th_cold = check_match(v1, v2, v3, v4)
                        if matching:
                            plist.append((th_cold, np.array([v1, v2, v3, v4])))
        print()
    except KeyboardInterrupt:
        print()
    except Exception as e:
        raise e
    finally:
        if not args.optimize:
            print(random.choice(plist)[1])
        else:
            th_array: np.ndarray[tuple[int], np.dtype[np.float64]] = np.array([
                i[0] for i in plist
            ])
            mindex: np.intp = np.argmin(th_array)
            print(plist[mindex][1])
        app = QApplication(sys.argv)
        win = MainWindow()
        win.show()

        sys.exit(app.exec())


if __name__ == '__main__':
    main()
