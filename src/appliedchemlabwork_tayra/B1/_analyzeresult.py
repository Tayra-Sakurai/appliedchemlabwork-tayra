"""Result analyzer."""
from ..common import *
import pandas
import numpy as np

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

    Notes
    -----
    The CSV file must be formed as following:

    +-------------+------------------------------+--------------+
    |  Substance  | Initial Amount or Solubility | Final Amount |
    +=============+==============================+==============+
    |    water    | 300.0                        | 274.2        |
    +-------------+------------------------------+--------------+
    |    alum     | 32.432                       | 6.903        |
    +-------------+------------------------------+--------------+
    | Solubility  | 11.4                         | 11.4         |
    +-------------+------------------------------+--------------+

    The table expresses the displayed table in Excel.
    """
    df: pandas.DataFrame = pandas.read_csv(
        filepath,
        header=0,
        index_col=0
    )
    vals: np.ndarray[tuple[int, int], np.dtype[np.float64]] = df.to_numpy()
    y: np.float64 = vals[1, 1] / ((vals[2, 2] / 100) * (vals[0,0] - vals[0,1]))
    data: dict[str, np.float64] = {
        "Initial Amount or Solubility": np.float64(0),
        "Final Amount": y,
    }
    df["Yield"] = data
    return df
