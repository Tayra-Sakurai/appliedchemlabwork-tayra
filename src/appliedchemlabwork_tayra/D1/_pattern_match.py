# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Pattern matching functions."""
import numpy as np
from typing import Any
from scipy.constants import R
__all__ = ['check_match']

VE1 = 2.00e-3
CE1 = 10.2
VB1 = 5.00e-3
CB1 = 6.0
VE2 = 10.0e-3
K2 = 7.23e-2
CHCL = 0.1
VHCL = 10.0e-3
VS = 25.0e-3
TEMP = 293.15
TS = 292
K2S = 7.23e-2
E_A = 4.6e4
VR = 250e-3
VMAX = 280e-3
TCOLD = 274.15


def check_match(
    v1: float | np.floating[Any],
    v2: float | np.floating[Any],
    v3: float | np.floating[Any],
    v4: float | np.floating[Any]
) -> tuple[bool, np.float64]:
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
    th_cold : float64
        The half life under the cold condition.

    Notes
    -----
    All parameters must be handed in litre.
    """
    # Ethyl acetate (mother solution)
    a1 = (VE1 * CE1) / (VE1 + v1)
    # The base
    b1 = (VB1 * CB1) / (VB1 + v2)
    # Reaction solutions.
    a2 = (VE2 * a1) / (v3 + v4 + VE2)
    b2 = (v4 * b1) / (v3 + v4 + VE2)
    bi = b2 - a2
    # The half life
    k2_warm: np.float64 = _calc_k2(TEMP)
    th_warm: np.float64 = _half_life_calc(a2, b2, bi, k2_warm)
    k2_cold = _calc_k2(TCOLD)
    th_cold: np.float64 = _half_life_calc(a2, b2, bi, k2_cold)
    # required volumes of the base for titrations and reactions.
    base_required1 = 5 * ((VHCL * CHCL) / b1)
    base_required2 = 2 * v3
    base_required3 = 12 * ((VHCL * CHCL - VS * bi) / b1)
    base_required = base_required1 + base_required2 + base_required3
    if (v2 + VB1) < (base_required * 1.1):
        return False, np.float64(0)
    if ((VE1 * 0.8 * 100) / v1) >= 7:
        return False, np.float64(0)
    if (th_warm / 60) <= 12:
        return False, np.float64(0)
    if (th_cold / 60) >= 60:
        return False, np.float64(0)
    if (VS * b2) >= (VHCL * CHCL):
        return False, np.float64(0)
    if (VE2 * a1) >= (v2 * b1):
        return False, np.float64(0)
    if ((VS * a2) / b1) <= 6e-3:
        return False, np.float64(0)
    if (v3 + v4 + VE2) <= VR:
        return False, np.float64(0)
    if (v3 + v4 + VE2) >= VMAX:
        return False, np.float64(0)
    if (v1 + VE1) <= (3 * VE2):
        return False, np.float64(0)
    return True, th_cold


def _calc_k2(temp: float) -> np.float64:
    """Calculates the k2 value.

    Parameters
    ----------
    temp : float
        The temperture.

    Returns
    -------
    k2 : float64
        The rate constant.
    """
    return K2S * np.exp(-((E_A / R) * (1 / temp - 1 / TS)))


def _half_life_calc(
    a2: float | np.floating[Any],
    b2: float | np.floating[Any],
    bi: float | np.floating[Any],
    k2: float | np.floating[Any]
) -> np.float64:
    """Calculates the half life.

    Parameters
    ----------
    a2 : floating value
        The initial concentration of ethyl acetate.
    b2 : floating value
        The initial concentration of NaOH.
    bi : floating value
        The terminal concentration of NaOH.
    k2 : floating value
        The value of pace coeffcient.

    Returns
    -------
    th : float64
        The half life of ethyl acetate.
    """
    return (np.log((a2 * b2 * 2 - a2 ** 2)/(a2 * b2))/bi)/k2
