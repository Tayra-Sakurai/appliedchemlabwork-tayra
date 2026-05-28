# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Calculation raw data script."""
__all__ = ['calc_required_amount_hcl', 'calc_concentration']


def calc_required_amount_hcl(
    concentration_hcl: float,
    concentration_base: float,
    volume_base: float = 25.0,
    n_oh: int = 1
) -> float:
    """Calculates the required amount of HCl aq.

    Parameters
    ----------
    concentration_hcl : float
        The concentration of HCl aq.
    concentration_base : float
        The concentration of the base to be titrated.
    volume_base : float, default 25.0
        The base volume.
    n_oh : int, default 1
        The valence of the base.

    Returns
    -------
    volume_hcl : float
        The required volume of HCl.
    """
    return (concentration_base * volume_base * n_oh) / concentration_hcl


def calc_concentration(
    conc_orig: float,
    vol_sol: float,
    vol_water: float
) -> float:
    """Calculates the concentration of diluted solvent.

    Parameters
    ----------
    conc_orig : float
        The original concentration of the solution.
    vol_sol : float
        The volume of the concentrated solution.
    vol_water : float
        The volume of pure water added to the solution.

    Returns
    -------
    conc_diluted : float
        The concentration of diluted solution.
    """
    return (conc_orig * vol_sol) / (vol_sol + vol_water)
