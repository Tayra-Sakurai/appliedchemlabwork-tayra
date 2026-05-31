"""Python module to calculate the result data."""
import pandas
import numpy as np
from typing import Any, overload
from scipy.constants import R
import numpy.typing as npt
import math

__all__ = ['ReactionData', 'calc_k_and_a', 'calc_ln']


class ReactionData:
    """Class to contain the data of reaction.

    Parameters
    ----------
    temp : float | floating[Any]
        The absolute temperture of the reaction.
    k : float | floating[Any]
        The pace coefficient of the reaction at the temperture of ``temp``.
    e_a : float | floating[Any]
        The activation energy of the reaction.

    Attributes
    ----------
    a : float | floating[Any]
        The frequency factor of the reaction.

    Methods
    -------
    get_k(temp=298.15)
        Gets the pace coefficient at the absolute temperture ``temp``.
    to_df()
        Generates a ``DataFrame``.
    """
    def __init__(
        self,
        temp: float | np.floating[Any],
        k: float | np.floating[Any],
        e_a: float | np.floating[Any]
    ) -> None:
        """Initializes the class.

        Parameters
        ----------
        temp : float | floating[Any]
            The tempreture.
        k : float | floating[Any]
            The coefficient at ``temp``.
        e_a : float | floating[Any]
            The activation energy.
        """
        self.temp = temp
        self.k = k
        self.e_a = e_a
        self.a: np.floating[Any] | float = k * np.exp(e_a / (R * temp))

    def get_k(
        self,
        temp: float | np.floating[Any] = 298.15
    ) -> float | np.floating[Any]:
        """Gets the pace coefficientat the temperture of ``temp``.

        Parameters
        ----------
        temp : float | floating[Any], default 298.15
            The temperture of the reaction environment.

        Returns
        -------
        k : float | floating[Any]
            The coefficient.
            As described before.
        """
        return self.a * np.exp(- (self.e_a / (R * temp)))
    
    def to_df(self) -> pandas.DataFrame:
        """Outputs the data as a ``DataFrame``.

        Returns
        -------
        df : DataFrame
            The table of the data.
        """
        data: dict[
            str,
            list[float | np.floating[Any]]
        ] = {
            'Activation Energy': [self.e_a],
            'Frequency Factor': [self.a],
            'Temperture': [self.temp],
            'k': [self.k],
        }
        df = pandas.DataFrame(data)
        return df
    

@overload
def calc_ln(
    base: float,
    bi: float | np.floating[Any]
) -> float | np.floating[Any]:
    return base * bi


@overload
def calc_ln(
    base: npt.NDArray[np.floating[Any]],
    bi: float | np.floating[Any]
) -> npt.NDArray[np.float64]:
    return np.log(base / (base - bi)) / bi


def calc_ln(
    base: float | np.floating[Any] | npt.NDArray[np.floating[Any]],
    bi: float | np.floating[Any]
):
    """Calculates the value of the factor.

    Parameters
    ----------
    base : float | floating[Any] | NDArray[floating[Any]]
        The concentration of the base.
    bi : float | floating[Any]
        The terminal concentration of the base.

    Returns
    -------
    value : float64
        The value of the factor.

    Notes
    -----
    The yielding value is

    .. math:: \\frac{1}{b_{\\infty}} \\ln \\frac{b -{} x}{a -{} x}

    where :math:`b` is the initial concentration of the base,
    :math:`a` is one of the ester,
    :math:`b_{\\infty}` is the terminal concentration of the base,
    and :math:`x` is the concentration of the reacted base.
    """
    if isinstance(base, (float, np.floating)):
        a_x = base - bi
        f = base / a_x
        return math.log(f) / bi
    if isinstance(base, np.ndarray):
        a_x = base - bi
        f = base / a_x
        return np.log(f) / bi


def calc_k_and_a(
    df: pandas.DataFrame
) -> npt.NDArray[np.floating[Any]]:
    """Calculates the rate constant.

    Parameters
    ----------
    df : DataFrame
        The data.

    Returns
    -------
    values : NDArray[floating[Any]]
        The value set of the result
        where the first column indicates the value of constant and
        the second one is the coefficient.

    Notes
    -----
    The table data must follow the following style.

    +------+---------------------------+
    | Time | Concentration of the base |
    +======+===========================+
    |  30  |          0.0153           |
    +------+---------------------------+
    |  320 |          0.0123           |
    +------+---------------------------+
    |  640 |          0.0103           |
    +------+---------------------------+
    | 1000 |          0.0089           |
    +------+---------------------------+
    | ...  |         ...               |
    +------+---------------------------+
    """
    t: pandas.Series[
        np.dtype[np.floating[Any] | np.integer[Any]]
    ] = df.iloc[:-1, 0]
    base: pandas.Series[np.dtype[np.floating[Any]]] = df.iloc[:-1, 1]
    bi = df.iloc[-1, 1]
    if isinstance(bi, np.floating):
        ls = calc_ln(base.to_numpy(), bi)
        return np.polynomial.polynomial.polyfit(t.to_numpy(), ls, deg=1)
    else:
        raise TypeError('Invalid type.')
