from src.appliedchemlabwork_tayra.D2 import calc_weight, calc_weighted_mean
import pytest
import numpy as np
from typing import Sequence
import pandas

def test_weight():
    a: dict[str, Sequence[float]] = {
        'pH': [6.5, 8.0, 9.0],
        'Flow-through, 280 nm': [0.118, 0.086, 0.035],
        'Eluted, 280 nm': [0.033, 0.065, 0.114],
        'Flow-through, 410 nm': [0.404, 0.285, 0.037],
        'Eluted, 410 nm': [0.015, 0.112, 0.318],
    }
    absorbance = pandas.DataFrame(data=a)
    source: dict[str, Sequence[float]] = {
        '280 nm': (0.093,),
        '410 nm': (0.461,),
    }
    data = pandas.DataFrame(source)
    print()
    print(calc_weighted_mean(data, absorbance).to_latex(index=False))
