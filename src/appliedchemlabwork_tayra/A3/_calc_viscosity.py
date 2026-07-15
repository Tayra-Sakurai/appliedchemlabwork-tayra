"""Calculates the viscosities."""
import numpy as np
import numpy.typing as npt
from typing import Any

__all__ = [
    "calc_relative_viscosity",
    "calc_specific_viscosity",
    "calc_inherent_viscosity",
    "calc_reduced_viscosity",
]


def calc_relative_viscosity(
    t: npt.NDArray[np.floating[Any]],
    t_0: float | np.floating[Any]
) -> npt.NDArray[np.floating[Any]]:
    """Calculates the relative viscosities.

    Parameters
    ----------
    t : NDArray[floating[Any]]
        The time of the flows.
    t_0 : Any floating number
        The time of the flows.

    Returns
    -------
    viscosity : NDArray[floating[Any]]
        The viscpsities.
    """
    return t / t_0


def calc_specific_viscosity(
    t: npt.NDArray[np.floating[Any]],
    t_0: float | np.floating[Any]
) -> npt.NDArray[np.floating[Any]]:
    """Calculates the specific viscosity.

    Parameters
    ----------
    t : NDArray[floating[Any]]
        The times elapsed while the solution flew down.
    t_0 : floating[Any] | float
        The time of the flow of the solvent.

    Returns
    -------
    specific : NDArray[Floating[Any]]
        The specific viscosities.
    """
    return (t - t_0) / t_0


def calc_inherent_viscosity(
    t: npt.NDArray[np.floating[Any]],
    c: npt.NDArray[np.floating[Any]],
    t_0: float | np.floating[Any]
) -> npt.NDArray[np.floating[Any]]:
    """Returns the inherent viscosity.

    Parameters
    ----------
    t : NDArray[floating[Any]]
    t_0 : floating[Any]
        Please see :func:`calc_relative_viscosity`.
    c : NDArray[floating[Any]]
        The concentrations of the solution.

    Returns
    -------
    viscosity : NDArray[floating[Any]]
        The viscosity.

    See Also
    --------
    calc_relative_viscosity : Detailed descriptions.

    Notes
    -----
    This function returns the values of inherent viscosities.

    .. math:: \\ln \\frac{\\iota_{\\mathrm{sp}}}{c}
    """
    return np.log(calc_relative_viscosity(t, t_0)) / c


def calc_reduced_viscosity(
    t: npt.NDArray[np.floating[Any]],
    c: npt.NDArray[np.floating[Any]],
    t_0: np.floating[Any] | float
) -> npt.NDArray[np.floating[Any]]:
    """Calculates the reduced viscosity.

    Parameters
    ----------
    t : NDArray[floating[Any]]
    t_0 : floating[Any]
        Please see ``calc_specific_viscosity``.
    c : NDArray[floating[Any]]
        The concentrations.

    Returns
    -------
    viscosity : NDArray[floating[Any]]
        The viscosities.

    See Also
    --------
    calc_specific_viscosity : Detailed descriptions.
    """
    return calc_specific_viscosity(t, t_0) / c
