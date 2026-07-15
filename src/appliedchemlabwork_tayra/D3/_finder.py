# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import cv2
from pathlib import Path
from ultralytics import YOLO
from ultralytics.engine.results import Results
import numpy as np
import polars as pl


def find_boxes(
    filepath: str,
    save_to: str,
    fsave: str = './runs/detect/predict',
):
    """Find bands as bounding boxes.

    Parameters
    ----------
    filepath : str
        The path to the image file containing the DNA electrophoresis bands.
    save_to : str
        The directory to save the data.
    fsave : str, optional
        The directory to save the result.

    Returns
    -------
    data : List of Results
        The list of the results.

    Raises
    ------
    FileNotFoundError
        The image file was not found.
    """
    model = YOLO("./trained-model/weights/best.pt")
    img = cv2.imread(filepath)
    if img is None:
        raise FileNotFoundError('The requested file was not found.')
    results: list[Results] = model(img, save=True, save_dir=fsave, conf=0.1)
    for i, result in enumerate(results):
        df = result.to_df()
        print(df)
        print(df[:, 'box'][0])
        df = df.with_columns(
            pl.col('box').struct.with_fields(
                x=pl.mean_horizontal(
                    pl.field('x1'),
                    pl.field('x2')
                ),
                y=pl.mean_horizontal(
                    pl.field('y1'),
                    pl.field('y2')
                )
            )
        )
        print(df.unnest("box"))
        df.unnest('box').write_csv(f'{save_to}/result-{i}.csv', include_bom=True)
    return results
