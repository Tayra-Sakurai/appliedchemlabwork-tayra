"""Pattern matching functions."""
import numpy as np
from typing import Any
__all__ = ['check_match']

ETHYL_ACETATE_SOURCE: float = 10.2
SODIUM_HYDROXIDE: float = 6.0
ETHYL_ACETATE_VOLUME: float = 2.0e-3
ETHYL_ACETATE_REACT: float = 10.0e-3
WATER_MIN: float = 700.
WATER_MAX: float = 1000.
SODIUM_VOL: float = 5.0e-3


def check_match(
    v1: float | np.floating[Any],
    v2: float | np.floating[Any],
    v3: float | np.floating[Any],
    v4: float | np.floating[Any]
) -> bool:
    """Checks if the point is in the territory.

    Parameters
    ----------
    v1 : float | np.floating[Any]
        The volume of ion exchanged water
        used to delute ethyl acetate solution.
    v2 : float | np.floating[Any]
        The volume of ion exchanged water
        used to delute sodium hydroxide solution.
    v3 : float | np.floating[Any]
        The volume of ion exchenged water
        used to delute reaction solution.
    v4 : float | np.floating[Any]
        The volume of NaOH aq for reaction.

    Returns
    -------
    match : bool
        ``True`` if the value fulfills the conditions;
        otherwise, ``False``.

    Notes
    -----
    All parameters must be handed in litre.
    """
    # Ethyl acetate
    a: float | np.floating[Any] = (
        ETHYL_ACETATE_VOLUME * ETHYL_ACETATE_SOURCE
        ) / (ETHYL_ACETATE_VOLUME + v1)
    c: float | np.floating[Any] = (SODIUM_HYDROXIDE * SODIUM_VOL) / (SODIUM_VOL + v2)
    b: float | np.floating[Any] = (v4 * c) / (v3 + v4 + ETHYL_ACETATE_REACT)
    d: float | np.floating[Any] = (ETHYL_ACETATE_REACT * a) / (v3 + v4 + ETHYL_ACETATE_REACT)
    if v2 < 700e-3:
        return False
    if v2 > 1:
        return False
    if (25e-3 * b) >= (10e-3 * 0.1):
        return False
    if (25e-3 * d) < (6e-3 * 0.1):
        return False
    if (v3 + v4 + ETHYL_ACETATE_REACT) > 280e-3:
        return False
    if (v4 * c) <= (ETHYL_ACETATE_REACT * a):
        return False
    if (v3 + v4 + ETHYL_ACETATE_REACT) <= 250e-3:
        return False
    return True
