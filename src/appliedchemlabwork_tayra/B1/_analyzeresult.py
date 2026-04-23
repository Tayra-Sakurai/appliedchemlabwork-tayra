"""Result analyzer."""
from ..common import *
import pandas
from typing import Any

__all__ = ["analyze"]


def analyze(
    filepath: str
) -> pandas.DataFrame:
    """Analyzes the result data.

    This adds the return rate column to the table of raw result.

    Parameters
    ----------
    filepath : str
        The path to the file to be read.

    Returns
    -------
    table : DataFrame
        The ``DataFrame`` instance of the table.
    """
    rawData: pandas.DataFrame = pandas.read_csv(filepath, header=0, index_col=0)
    start_materials: pandas.Series[Any] = rawData.iloc[:,1]
    results: pandas.Series[Any] = rawData.iloc[:,2]

