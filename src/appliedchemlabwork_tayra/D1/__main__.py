# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from typing import NoReturn
from PyQt6.QtWidgets import QApplication
from ._widgets import *
import sys


def main() -> NoReturn:
    app = QApplication(sys.argv)
    m_window = _MainWindow()
    m_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
