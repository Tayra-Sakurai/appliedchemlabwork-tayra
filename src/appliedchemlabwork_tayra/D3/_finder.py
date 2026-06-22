# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import cv2
from typing import Any
from ultralytics import YOLO


def find_boxes(
    filepath: str
):
    """Find bands as bounding boxes.

    Parameters
    ----------
    filepath : str
        The path to the image file containing the DNA electrophoresis bands.

    Returns
    -------
    data : The bounding boxes
        The bounding boxes.

    Raises
    ------
    FileNotFoundError
        The image file was not found.
    """
    model = YOLO("./trained-model/weights/last.pt")
    img = cv2.imread(filepath)
    if img is None:
        raise FileNotFoundError('The requested file was not found.')
    nimg = cv2.convertScaleAbs(img, alpha=1.5)
    model(nimg, save=True)
