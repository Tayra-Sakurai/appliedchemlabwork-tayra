# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
__all__ = ["calc_return_rate"]


def calc_return_rate(
    initialamount: float,
    result: float
) -> float:
    """Calculates the reward rate of the experiment.

    Parameters
    ----------
    initialamount : float
        The initial amount of the reactant.
    result : float
        The resulted amount.

    Returns
    -------
    rate : float
        The resulted rate.

    Raises
    ------
    RuntimeError
        `result` is larger than `initialamount`.
    """
    if initialamount < result:
        raise RuntimeError(
            "Initial amount of reactant must be the restricted one's."
        )
    return result / initialamount
