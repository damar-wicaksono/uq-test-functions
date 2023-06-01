"""
Module with an implementation of the (third) Franke function.

The (third) Franke function is a two-dimensional scalar-valued function.
The function was first introduced in [1] in the context of interpolation
problem. It features a saddle shaped surface.

The Franke's original report [1] contains in total six two-dimensional test
functions. The first function that appeared in the report is commonly known
as the "Franke function".

References
----------

1. Richard Franke, "A critical comparison of some methods for interpolation
   of scattered data," Naval Postgraduate School, Monterey, Canada,
   Technical Report No. NPS53-79-003, 1979.
   URL: https://core.ac.uk/reader/36727660
"""
import numpy as np

from typing import Optional

from ..core.prob_input.univariate_distribution import UnivDist
from ..core.uqtestfun_abc import UQTestFunABC
from .available import create_prob_input_from_available

__all__ = ["Franke3"]

INPUT_MARGINALS_FRANKE1979 = [  # From Ref. [1]
    UnivDist(
        name="X1",
        distribution="uniform",
        parameters=[0.0, 1.0],
    ),
    UnivDist(
        name="X2",
        distribution="uniform",
        parameters=[0.0, 1.0],
    ),
]

AVAILABLE_INPUT_SPECS = {
    "Franke1979": {
        "name": "Franke-1979",
        "description": (
            "Input specification for the (third) Franke function "
            "from Franke (1979)."
        ),
        "marginals": INPUT_MARGINALS_FRANKE1979,
        "copulas": None,
    }
}

DEFAULT_INPUT_SELECTION = "Franke1979"


class Franke3(UQTestFunABC):
    """A concrete implementation of the (first) Franke function."""

    _TAGS = ["metamodeling"]

    _AVAILABLE_INPUTS = tuple(AVAILABLE_INPUT_SPECS.keys())

    _AVAILABLE_PARAMETERS = None

    _DEFAULT_SPATIAL_DIMENSION = 2

    _DESCRIPTION = "(Third) Franke function from Franke (1979)"

    def __init__(
        self,
        *,
        prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
        name: Optional[str] = None,
        rng_seed_prob_input: Optional[int] = None,
    ):
        # --- Arguments processing
        prob_input = create_prob_input_from_available(
            prob_input_selection,
            AVAILABLE_INPUT_SPECS,
            rng_seed=rng_seed_prob_input,
        )
        # Process the default name
        if name is None:
            name = Franke3.__name__

        super().__init__(prob_input=prob_input, name=name)

    def evaluate(self, xx: np.ndarray):
        """Evaluate the (third) Franke function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            Two-Dimensional input values given by N-by-2 arrays where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the (third) Franke function evaluated
            on the input values.
            The output is a 1-dimensional array of length N.
        """
        # Compute the (third) Franke function
        term_1 = 1.25 + np.cos(5.4 * xx[:, 1])
        term_2 = 6 * (1 + (3 * xx[:, 0] - 1) ** 2)

        yy = term_1 / term_2

        return yy