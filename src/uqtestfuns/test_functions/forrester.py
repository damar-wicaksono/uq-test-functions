"""
Module with an implementation of the Forrester et al. (2008) test function.

The Forrester2008 test function is a one-dimensional scalar-valued function.
The function is multimodal, with a single global minimum, a single local
minimum, and a zero-gradient at the inflection point.

References
----------

1. William J. Welch, Robert J. Buck, Jerome Sacks, Henry P. Wynn,
   Toby J. Mitchell, and Max D. Morris, "Screening, predicting, and computer
   experiments," Technometrics, vol. 34, no. 1, pp. 15-25, 1992.
   DOI: 10.2307/1269548
"""
import numpy as np

from ..core.prob_input.input_spec import UnivDistSpec, ProbInputSpecFixDim
from ..core.uqtestfun_abc import UQTestFunABC

__all__ = ["Forrester2008"]

AVAILABLE_INPUT_SPECS = {
    "Forrester2008": ProbInputSpecFixDim(
        name="Forrester2008",
        description=(
            "Input specification for the 1D test function "
            "from Forrester et al. (2008)"
        ),
        marginals=[
            UnivDistSpec(
                name="x",
                distribution="uniform",
                parameters=[0, 1],
                description="None",
            )
        ],
        copulas=None,
    ),
}


def evaluate(xx: np.ndarray) -> np.ndarray:
    """The evaluation function for the Forrester et al. (2008) function.

    Parameters
    ----------

    """
    return (6 * xx - 2) ** 2 * np.sin(12 * xx - 4)


class Forrester2008(UQTestFunABC):
    """An implementation of the 1D function of Forrester et al. (2008)."""

    _tags = ["optimization", "metamodeling"]
    _description = "One-dimensional function from Forrester et al. (2008)"
    _available_inputs = AVAILABLE_INPUT_SPECS
    _available_parameters = None
    _default_spatial_dimension = 1

    eval_ = staticmethod(evaluate)
