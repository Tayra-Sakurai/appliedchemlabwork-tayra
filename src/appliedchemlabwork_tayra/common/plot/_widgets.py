# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""The widgets."""
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtGraphs import QScatterSeries
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QFormLayout, QVBoxLayout, QGroupBox, QFileDialog, QGraphicsScene, QGraphicsView
import pandas
from ._plot import generate_points

__all__ = ['SpecialWindow', 'CentralWidget']


class SpecialWindow(QMainWindow):
    """Special GUI window for all plotting actions.

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget.
    flags : WindowType, optional
        The window flags.
    """
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window
    ) -> None:
        super().__init__(parent, flags)
        self.setCentralWidget(CentralWidget(self))


class CentralWidget(QWidget):
    """Main window's central widget.

    Parameters
    ----------
    parent : QWidget
        The parent window.

    Attributes
    ----------
    btn_1 : QPushButton
        The file picking button.
    btn_2 : QPushButton
        The execution button.
    file_path : str
        The string path to the csv file.

    Methods
    -------
    initializeComponent()
        The component initializer.
    """
    file_path: str = ''

    def __init__(
        self,
        parent: QWidget
    ):
        super().__init__(parent)
        self.initializeComponent()

    def initializeComponent(self):
        """Initializes the components."""
        mainLayout = QVBoxLayout(self)
        mainBox = QGroupBox('設定', self)
        layout = QFormLayout(mainBox)

        label1 = QLabel('ファイルを選択', mainBox)
        self.btn_1 = QPushButton('ファイルをここで選択します', mainBox)
        self.btn_1.clicked.connect(self._setPath)
        layout.addRow(label1, self.btn_1)
        label2 = QLabel('実行', mainBox)
        self.btn_2 = QPushButton('実行', mainBox)
        self.btn_2.clicked.connect(self._exec_plot)
        layout.addRow(label2, self.btn_2)

        mainLayout.addWidget(mainBox)
        self.graph = QGraphicsScene()
        gView = QGraphicsView(self.graph)
        mainLayout.addWidget(gView)

    def _setPath(
        self
    ) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self.parentWidget(),
            'データファイルを選択',
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),
            'CSV file (*.csv)'
        )
        self.file_path = path

    def _exec_plot(
        self
    ) -> None:
        """Plot the values."""
        df = pandas.read_csv(
            self.file_path,
            encoding='utf_8_sig',
            header=0
        )
        points = generate_points(df)
        series = QScatterSeries(self.graph)
        for point in points:
            series.append(float(point[0]), float(point[1]))
        series.show()
