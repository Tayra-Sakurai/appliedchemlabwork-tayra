# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from ._widgets import SpecialWindow
from PyQt6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    w = SpecialWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
