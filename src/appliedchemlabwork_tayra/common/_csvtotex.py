import pandas
from os import PathLike
from typing import Any

__all__ = ["csv_to_latex"]

def csv_to_latex(
    file: PathLike[Any] | str
) -> str:
    """Converts the CSV data into a LaTeX code.

    Extended Summary
    ----------------
    Converts CSV table into LaTeX ``\\tabular``
    environment code via ``pandas``.

    Parameters
    ----------
    file: PathLike | str
        The path-like object or the path string
        to the CSV file to be converted.

    Returns
    -------
    tex_code: str
        The LaTeX code of the table.

    Notes
    -----
    In LaTeX, the table as following:

    +---------+-----------+-----------+
    | Header  | Header 1  | Header 2  |
    +=========+===========+===========+
    | Content | Content 2 | Content 3 |
    | Content | Content 4 | Content 5 |
    +---------+-----------+-----------+

    is equivalent to:

    .. code-block:: latex
       \\begin{tabular}[|c|c|c|]
           \\hline
           Header & Header 1 & Header 2\\\\
           \\hline
           Content & Content 2 & Content 3\\\\
           Content & Content 4 & Content 5\\\\
           \\hline
       \\end{tabular}

    Examples
    --------
    >>> from appliedchemlabwork_tayra import common
    >>> common.csv_to_latex('data.csv')
    "\\\\begin{tabular}\\n...\\\\end{tabular}"
    """
    df: pandas.DataFrame = pandas.read_csv(file)
    tex_code: str = df.to_latex()
    return tex_code
