import pandas
import numpy as np
from typing import Any, Union
from ._calc_mw import *
from ._calc_viscosity import *
import matplotlib.pyplot as plt
from os import PathLike

__all__ = ['DataSet', 'get_data', 'plot_and_process_data']

type _Float1D = np.ndarray[
    tuple[int],
    np.dtype[np.floating[Any]]
]

type _Float2D = np.ndarray[
    tuple[int, int],
    np.dtype[np.floating[Any]]
]

type _AnyFloat = Union[
    float,
    np.floating[Any]
]


class DataSet:
    """Base class for input data of this module.
    
    Parameters
    ----------
    solution_conc : float | floating[Any]
        The concentration of the solution.
    K : float | floating[Any]
        The ``K`` coefficient of Mark-Houwink-Sakurada's equation.
    alpha : float | floating[Any]
        The ``alpha`` coefficient.
    vol_sol : _Float1D
        The volumes of the solution.
    vol_solvent : _Float1D
        The volumes of pure solvent.
    t_0 : float | floating[Any]
        The passage time.
    t : _Float2D
        The times.

    Attributes
    ----------
    concs : _Float1D
        The concentrations.
    times : _Float1D
        The times elapsed while pass between the lines.
    """
    def __init__(
        self,
        solution_conc: _AnyFloat,
        K: _AnyFloat,
        alpha: _AnyFloat,
        vol_sol: _Float1D,
        vol_solvent: _Float1D,
        t_0: _AnyFloat,
        t: _Float2D
    ) -> None:
        self.solution_conc = solution_conc
        self.K = K
        self.alpha = alpha
        self.vol_sol = vol_sol
        self.vol_solvent = vol_solvent
        self.t_0 = t_0
        self.t = t
        self.concs: _Float1D = ((vol_sol - vol_solvent) * solution_conc) / vol_sol
        self.times: _Float1D = np.nanmean(t, axis=1)


def get_data(
    df_sol: pandas.DataFrame,
    df_res: pandas.DataFrame
) -> DataSet:
    """Loads the data.

    Parameters
    ----------
    df_sol : DataFrame
        The solution data table.
    df_res : DataFrame
        The result data table.
    """
    sol_data: pandas.Series[np.float64] = df_sol.iloc[0]
    print(sol_data.dtype)
    solution_conc = (sol_data.iloc[0] / sol_data.iloc[1]) * 100
    print(solution_conc)
    k, alpha = sol_data.iloc[2:4]
    res_solv: pandas.Series[np.float64] = df_res.iloc[0]
    t_0 = np.nanmean(res_solv[2:].to_numpy())
    result_data = df_res.iloc[1:]
    vol_sol: _Float1D = result_data.iloc[:, 0].to_numpy()
    vol_solvent: _Float1D = result_data.iloc[:, 1].to_numpy()
    t: _Float2D = result_data.iloc[:, 2:].to_numpy()
    return DataSet(
        solution_conc,
        k,
        alpha,
        vol_sol,
        vol_solvent,
        t_0,
        t
    )


def plot_and_process_data(
    ds: DataSet,
    dest1: PathLike[Any],
    dest2: PathLike[Any]
) -> None:
    """Plots the data.

    Parameters
    ----------
    ds : DataSet
        The data set.
    dest : PathLike[Any]
        The destination file.
    """
    print(ds.times)
    print(ds.concs)
    print(ds.times / ds.t_0)
    _, ax = plt.subplots()
    ax.axvline(color='k')
    ax.grid(True)
    y1 = calc_reduced_viscosity(
        ds.times,
        ds.concs,
        ds.t_0
    )
    x = ds.concs
    ax.plot(x, y1, '.', label='$\\eta_{\\mathrm{red}} / \\text{g} \\left( 100\\ \\text{mL}\\right)^{-1}$', color='C0')
    y2 = calc_inherent_viscosity(
        ds.times,
        ds.concs,
        ds.t_0
    )
    ax.plot(x, y2, '.', label='$\\eta_{\\mathrm{inh}} / \\text{g} \\left( 100\\ \\text{mL}\\right)^{-1}$', color='C1')
    b, a1, a2 = calc_intrisic_viscosity(
        ds.concs,
        y1,
        y2
    )
    print(b, a1, a2)
    ax.axline((0., float(b)), slope=float(a1), color='C0')
    ax.axline((0., float(b)), slope=float(a2), color='C1')
    ax.legend()
    ax.set_xlabel('$c / \\text{g}\\ \\left(100 \\ \\text{mL}\\right)$')
    ax.set_ylabel('$\\eta / \\text{g} \\left( 100\\ \\text{mL}\\right)^{-1}$')
    plt.show()
    eta_r = calc_relative_viscosity(ds.times, ds.t_0)
    eta_sp = calc_specific_viscosity(ds.times, ds.t_0)
    df1 = pandas.DataFrame(
        data={
            't (Average) / s': ds.times,
            'c / g (100 mL)^(-1)': ds.concs,
            'Eta_r': eta_r,
            'Eta_sp': eta_sp,
            'Eta_red / (100 mL) g^(-1)': y1,
            'Eta_inh / (100 mL) g^(-1)': y2,
        }
    )
    df1.to_csv(
        dest1,
        index=False,
        encoding='utf_8_sig',
        lineterminator='\r\n'
    )
    df2 = pandas.DataFrame(
        data={
            't_0 / s': (ds.t_0,),
            'm.w.': (calc_mw(b, ds.K, ds.alpha),),
            '[Eta] / (100 mL) g^(-1)': (b,),
            'k[Eta]^2': (a1,),
            'Beta [Eta]^2': (a2,),
        }
    )
    df2.to_csv(
        dest2,
        lineterminator='\r\n',
        encoding='utf_8_sig'
    )
