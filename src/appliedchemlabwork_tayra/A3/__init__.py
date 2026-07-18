"""Calculation and plotting module for A3 experiment.

Subpackages
-----------

.. autosummary::
   :toctree: generated/

   calc_relative_viscosity
   calc_specific_viscosity
   calc_inherent_viscosity
   calc_reduced_viscosity
   calc_intrisic_viscosity
   calc_mw
   DataSet
   get_data
   plot_and_process_data
"""
from ._calc_viscosity import *
from ._calc_mw import *
from ._loader import *
