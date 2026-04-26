# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Runner module program."""
from ._analyzeresult import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas


def main() -> None:
    """Runs the module as a script.

    Notes
    -----
    This is for only command-line calling.
    """
    fname: str = askopenfilename(
        title="Please select the file to load.",
        filetypes=(
            (
                "Comma-Separated Values",
                (
                    "*.csv",
                    "*.txt",
                )
            ),
        ),
        defaultextension=".csv"
    )
    result: pandas.DataFrame = analyze(fname)
    savefilename: str = asksaveasfilename(
        title="Please select the file to be saved",
        defaultextension=".csv",
        filetypes=(
            (
                "Comma-Separated Values",
                (
                    "*.csv",
                    "*.txt",
                ),
            ),
            (
                "Any Files",
                "*.*",
            ),
        )
    )
    result.to_csv(savefilename)


if __name__ == "__main__":
    main()
