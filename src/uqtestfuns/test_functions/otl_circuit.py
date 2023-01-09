"""
Module with an implementation of the OTL circuit test function.

The OTL circuit test function is a six-dimensional scalar-valued function
that computes the mid-point voltage
of an output transformerless (OTL) push-pull circuit.
The function has been used as a test function in metamodeling exercises [1].
A 20-dimensional variant was used for sensitivity analysis in [2]
by introducing 14 additional inert input variables.

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


DEFAULT_NAME = "OTL"

DEFAULT_INPUT_MARGINALS_BEN_ARI = [
    UnivariateInput(
        name="Rb1",
        distribution="uniform",
        parameters=[50.0, 150.0],
        description="Resistance b1 [kOhm]",
    ),
    UnivariateInput(
        name="Rb2",
        distribution="uniform",
        parameters=[25.0, 70.0],
        description="Resistance b2 [kOhm]",
    ),
    UnivariateInput(
        name="Rf",
        distribution="uniform",
        parameters=[0.5, 3.0],
        description="Resistance f [kOhm]",
    ),
    UnivariateInput(
        name="Rc1",
        distribution="uniform",
        parameters=[1.2, 2.5],
        description="Resistance c1 [kOhm]",
    ),
    UnivariateInput(
        name="Rc2",
        distribution="uniform",
        parameters=[0.25, 1.20],
        description="Resistance c2 [kOhm]",
    ),
    UnivariateInput(
        name="beta",
        distribution="uniform",
        parameters=[50.0, 300.0],
        description="Current gain [A]",
    ),
]

DEFAULT_INPUT_MARGINALS_MOON = [
    copy(_) for _ in DEFAULT_INPUT_MARGINALS_BEN_ARI
]
for i in range(14):
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
        (At least) 6-dimensional input values given by N-by-6 arrays
        where N is the number of input values.

    Returns
    -------
    np.ndarray
        The output of the OTL circuit test function,
        i.e., the mid-point voltage in Volt.
        The output is a one-dimensional array of length N.

    Notes
    -----
    - The variant of this test function has 14 additional inputs,
      but they are all taken to be inert and therefore should not affect
      the output.
    """
    rr_b1 = xx[:, 0]  # Resistance b1
    rr_b2 = xx[:, 1]  # Resistance b2
    rr_f = xx[:, 2]  # Resistance f
    rr_c1 = xx[:, 3]  # Resistance c1
    rr_c2 = xx[:, 4]  # Resistance c2
    beta = xx[:, 5]  # Current gain

    # Compute the voltage across b1
    vb1 = 12 * rr_b1 / (rr_b1 + rr_b2)

    # Compute the mid-point voltage
    denom = beta * (rr_c2 + 9) + rr_f
    term_1 = ((vb1 + 0.74) * beta * (rr_c2 + 9)) / denom
    term_2 = 11.35 * rr_f / denom
    term_3 = 0.74 * rr_f * beta * (rr_c2 + 9) / (rr_c1 * denom)

    vm = term_1 + term_2 + term_3

    return vm