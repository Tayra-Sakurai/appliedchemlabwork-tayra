# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import cv2
from typing import Any
from os import PathLike
from tkinter.filedialog import askopenfilename


def detect_band(
    path: str
):
    """Loads the bands of the sequence.

    Parameters
    ----------
    path : StrOrPath
        The path to the image file.

    Raises
    ------
    FileNotFoundError
        The file was not found.
    """
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError('Requested file does not exist.')
    # Detect the gel zone.
    edge1 = cv2.Canny(img, 10, 50)



if __name__ == '__main__':
    f = askopenfilename(
        title='Hello',
        filetypes=(
            (
                'JPEG Image',
                (
                    '*.jpg',
                    '*.jpeg',
                ),
            ),
        ),
        defaultextension='.jpg'
    )
    detect_band(f)
