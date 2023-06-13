"""
Module with an implementation of the Welch et al. (1992) test function.

The Welch1992 test function is a 20-dimensional scalar-valued function.
The function features some strong non-linear effects as well as some pair
interaction effects. Furthermore, two input variables (namely x8 and x16)
are inert.

The function was introduced in [1] as a test function for metamodeling and
sensitivity analysis purposes. The function is also suitable for testing
multi-dimensional integration algorithms.

References
----------

1. William J. Welch, Robert J. Buck, Jerome Sacks, Henry P. Wynn,
   Toby J. Mitchell, and Max D. Morris, "Screening, predicting, and computer
   experiments," Technometrics, vol. 34, no. 1, pp. 15-25, 1992.
   DOI: 10.2307/1269548
"""
import numpy as np

from typing import Optional

from ..core.prob_input.input_spec import MarginalSpec, ProbInputSpec
from ..core.uqtestfun_abc import UQTestFunABC
from .available import get_prob_input_spec, create_prob_input_from_spec

__all__ = ["Welch1992"]


INPUT_MARGINALS_WELCH1992 = [
    MarginalSpec(
        name=f"x{i}",
        distribution="uniform",
        parameters=[-0.5, 0.5],
        description="None",
    )
    for i in range(1, 20 + 1)
]

AVAILABLE_INPUT_SPECS = {
    "Welch1992": ProbInputSpec(
        name="Welch1992",
        description=(
            "Input specification for the test function "
            "from Welch et al. (1992)"
        ),
        marginals=INPUT_MARGINALS_WELCH1992,
        copulas=None,
    ),
}

DEFAULT_INPUT_SELECTION = "Welch1992"


class Welch1992(UQTestFunABC):
    """A concrete implementation of the Welch et al. (1992) test function."""

    _tags = ["metamodeling", "sensitivity", "integration"]

    _available_inputs = tuple(AVAILABLE_INPUT_SPECS.keys())

    _available_parameters = None

    _default_spatial_dimension = 20

    _description = "20-Dimensional function from Welch et al. (1992)"

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        name: Optional[str] = None,
        rng_seed_prob_input: Optional[int] = None,
    ):
        # --- Arguments processing
        # Get the ProbInputSpec from available
        prob_input_spec = get_prob_input_spec(
            prob_input_selection, AVAILABLE_INPUT_SPECS
        )
        # Create a ProbInput
        prob_input = create_prob_input_from_spec(
            prob_input_spec, rng_seed=rng_seed_prob_input
        )
        # Process the default name
        if name is None:
            name = self.__class__.__name__

        super().__init__(prob_input=prob_input, name=name)

    def evaluate(self, xx: np.ndarray):
        """Evaluate the Welch et al. (1992) function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            1-Dimensional input values given by an N-by-1 array
            where N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the test function evaluated on the input values.
            The output is a 1-dimensional array of length N.

        Notes
        -----
        - The input variables xx[:, 7] (x8) and xx[:, 15] (x16) are inert and
          therefore, does not appear in the computation below.
        """
        yy = (
            (5 * xx[:, 11]) / (1 + xx[:, 0])
            + 5 * (xx[:, 3] - xx[:, 19]) ** 2
            + xx[:, 4]
            + 40 * xx[:, 18] ** 3
            - 5 * xx[:, 18]
            + 0.05 * xx[:, 1]
            + 0.08 * xx[:, 2]
            - 0.03 * xx[:, 5]
            + 0.03 * xx[:, 6]
            - 0.09 * xx[:, 8]
            - 0.01 * xx[:, 9]
            - 0.07 * xx[:, 10]
            + 0.25 * xx[:, 12] ** 2
            - 0.04 * xx[:, 13]
            + 0.06 * xx[:, 14]
            - 0.01 * xx[:, 16]
            - 0.03 * xx[:, 17]
        )

        return yy
