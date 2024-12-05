"""
Module with an implementation of the functions from Linkletter et al. (2006)

The paper by Linkletter et al. (2006) [1] contains four analytical test
functions used for sensitivity analysis in the context of variable selection
in Gaussian process metamodeling.
All functions are defined in ten dimensions but some of them are inactive.

Available functions are:

- Linear function with four active input variables..
- Linear function with decreasing coefficients, eight active input variables.

References
----------

1. C. Linkletter, D. Bingham, N. Hengartner, D. Higdon, and K. Q. Ye,
   “Variable Selection for Gaussian Process Models in Computer Experiments,”
   Technometrics, vol. 48, no. 4, pp. 478–490, 2006.
   DOI: 10.1198/004017006000000228.
"""

import numpy as np

from uqtestfuns.core.custom_typing import ProbInputSpecs
from uqtestfuns.core.uqtestfun_abc import UQTestFunFixDimABC

__all__ = ["LinkletterLinear", "LinkletterDecCoeffs"]


def evaluate_linear(xx: np.ndarray) -> np.ndarray:
    """Evaluate the linear function from Linkletter et al. (2006).

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-10 array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    yy = 0.2 * np.sum(xx[:, :4], axis=1)

    return yy


def evaluate_dec_coeffs(xx: np.ndarray) -> np.ndarray:
    """Evaluate the linear function with decreasing coefficients.

    Parameters
    ----------
    xx : np.ndarray
        M-Dimensional input values given by an N-by-10 array where
        N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the test function evaluated on the input values.
        The output is a 1-dimensional array of length N.
    """
    exps = np.arange(8)  # 8 input variables are active
    coeffs = 0.2 / 2**exps

    yy = np.sum(coeffs * xx[:, :8], axis=1)

    return yy


class LinkletterLinear(UQTestFunFixDimABC):
    """A concrete implementation of the linear function."""

    _tags = ["metamodeling", "sensitivity"]
    _description = "Linear function from Linkletter et al. (2006)"
    _available_inputs: ProbInputSpecs = {
        "Linkletter2006": {
            "function_id": "LinkletterLinear",
            "description": (
                "Input specification for the linear test function Eq. (5)"
                "from Linkletter et al. (2006)"
            ),
            "marginals": [
                {
                    "name": f"x_{i + 1}",
                    "distribution": "uniform",
                    "parameters": [0, 1],
                    "description": None,
                }
                for i in range(10)
            ],
            "copulas": None,
        },
    }
    _available_parameters = None

    evaluate = staticmethod(evaluate_linear)  # type: ignore


class LinkletterDecCoeffs(UQTestFunFixDimABC):
    """A concrete implementation of the linear with decreasing coefficients."""

    _tags = ["metamodeling", "sensitivity"]
    _description = (
        "Linear function with decreasing coefficients from Linkletter et al. "
        "(2006)"
    )
    _available_inputs: ProbInputSpecs = {
        "Linkletter2006": {
            "function_id": "LinkletterLinear",
            "description": (
                "Input specification for the linear test function with "
                "decreasing coefficients Eq. (6) from Linkletter et al. (2006)"
            ),
            "marginals": [
                {
                    "name": f"x_{i + 1}",
                    "distribution": "uniform",
                    "parameters": [0, 1],
                    "description": None,
                }
                for i in range(10)
            ],
            "copulas": None,
        },
    }
    _available_parameters = None

    evaluate = staticmethod(evaluate_dec_coeffs)  # type: ignore
