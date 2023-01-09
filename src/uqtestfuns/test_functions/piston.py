"""
Module with an implementation of the Piston simulation test function.

The Piston simulation test function is a seven-dimensional scalar-valued
test function.
The function computes the cycle time of a piston.
The function has been used as a test function in metamodeling exercises [1].
A 20-dimensional variant was used for sensitivity analysis in [2]
by introducing 13 additional inert input variables.

References
----------

1. E. N. Ben-Ari and D. M. Steinberg, "Modeling data from computer
   experiments: An empirical comparison of Kriging with MARS
   and projection pursuit regression," Quality Engineering,
   vol. 19, pp. 327-338, 2007.
   DOI: 10.1080/08982110701580930
2. H. Moon, "Design and Analysis of Computer Experiments for Screening Input
   Variables," Ph. D. dissertation, Ohio State University, Ohio, 2010.
   URL: http://rave.ohiolink.edu/etdc/view?acc_num=osu1275422248
"""
import numpy as np

from copy import copy

from ..core import UnivariateInput, MultivariateInput


DEFAULT_NAME = "Piston"

# Input specification from [1]
DEFAULT_INPUT_MARGINALS_BEN_ARI = [
    UnivariateInput(
        name="M",
        distribution="uniform",
        parameters=[30.0, 60.0],
        description="Piston weight [kg]",
    ),
    UnivariateInput(
        name="S",
        distribution="uniform",
        parameters=[0.005, 0.020],
        description="Piston surface area [m^2]",
    ),
    UnivariateInput(
        name="V0",
        distribution="uniform",
        parameters=[0.002, 0.010],
        description="Initial gas volume [m^3]",
    ),
    UnivariateInput(
        name="k",
        distribution="uniform",
        parameters=[1000.0, 5000.0],
        description="Spring coefficient [N/m]",
    ),
    UnivariateInput(
        name="P0",
        distribution="uniform",
        parameters=[90000.0, 110000.0],
        description="Atmospheric pressure [N/m^2]",
    ),
    UnivariateInput(
        name="Ta",
        distribution="uniform",
        parameters=[290.0, 296.0],
        description="Ambient temperature [K]",
    ),
    UnivariateInput(
        name="T0",
        distribution="uniform",
        parameters=[340.0, 360.0],
        description="Filling gas temperature [K]",
    ),
]

# Input specification from [2]
DEFAULT_INPUT_MARGINALS_MOON = [
    copy(_) for _ in DEFAULT_INPUT_MARGINALS_BEN_ARI
]
for i in range(13):
    DEFAULT_INPUT_MARGINALS_MOON.append(
        UnivariateInput(
            name=f"Inert {i+1}",
            distribution="uniform",
            parameters=[100.0, 200.0],
            description="Inert input [-]",
        )
    )

DEFAULT_INPUTS = {
    "ben-ari": MultivariateInput(DEFAULT_INPUT_MARGINALS_BEN_ARI),
    "moon": MultivariateInput(DEFAULT_INPUT_MARGINALS_MOON),
}

DEFAULT_INPUT_SELECTION = "ben-ari"

DEFAULT_PARAMETERS = None


def evaluate(xx: np.ndarray) -> np.ndarray:
    """Evaluate the OTL circuit test function on a set of input values.

    Parameters
    ----------
    xx : np.ndarray
        (At least) 7-dimensional input values given by N-by-7 arrays
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the Piston simulation test function,
        i.e., the cycle time in seconds.
        The output is a one-dimensional array of length N.

    Notes
    -----
    - The variant of this test function has 14 additional inputs,
      but they are all taken to be inert and therefore should not affect
      the output.
    """
    mm = xx[:, 0]  # piston weight
    ss = xx[:, 1]  # piston surface area
    vv_0 = xx[:, 2]  # initial gas volume
    kk = xx[:, 3]  # spring coefficient
    pp_0 = xx[:, 4]  # atmospheric pressure
    tt_a = xx[:, 5]  # ambient temperature
    tt_0 = xx[:, 6]  # filling gas temperature

    # Compute the force
    aa = pp_0 * ss + 19.62 * mm - kk * vv_0 / ss

    # Compute the force difference
    daa = np.sqrt(aa**2 + 4.0 * kk * pp_0 * vv_0 * tt_a / tt_0) - aa

    # Compute the volume difference
    vv = ss / 2.0 / kk * daa

    # Compute the cycle time
    cc = (
        2.0
        * np.pi
        * np.sqrt(mm / (ss**2 * pp_0 * vv_0 * tt_a / tt_0 / vv**2))
    )

    return cc
