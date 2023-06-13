"""
Module with an implementation of the Bratley et al. (1992) test functions.

The Bratley et al. (1992) paper [1] contains four M-dimensional scalar-valued
functions for testing multi-dimensional numerical integrations using low
discrepancy sequences. The functions was used in [2] and [3] in the context
of global sensitivity analysis.

The four functions are:

- Bratley1992d: A sum of products integrand; integration test function #4

The Bratley1992d function may also be referred to as the "Bratley function"
or "Bratley et al. (1992) function" in the literature.

References
----------

1. Paul Bratley, Bennet L. Fox, and Harald Niederreiter, "Implementation and
   tests of low-discrepancy sequences," ACM Transactions on Modeling and
   Computer Simulation, vol. 2, no. 3, pp. 195-213, 1992.
   DOI:10.1145/146382.146385
2. S. Kucherenko, M. Rodriguez-Fernandez, C. Pantelides, and N. Shah,
   “Monte Carlo evaluation of derivative-based global sensitivity measures,”
   Reliability Engineering & System Safety, vol. 94, pp. 1137–1148, 2009.
   DOI:10.1016/j.ress.2008.05.006
3. A. Saltelli, P. Annoni, I. Azzini, F. Campolongo, M. Ratto,
   and S. Tarantola, “Variance based sensitivity analysis of model output.
   Design and estimator for the total sensitivity index,” Computer Physics
   Communications, vol. 181, no. 2, pp. 259–270, 2010,
   DOI:10.1016/j.cpc.2009.09.018
"""
import numpy as np

from typing import List, Optional

from ..core.uqtestfun_abc import UQTestFunABC
from ..core.prob_input.univariate_distribution import UnivDist
from .available import create_prob_input_from_available

__all__ = ["Bratley1992d"]


def _bratley_input(spatial_dimension: int) -> List[UnivDist]:
    """Create a list of marginals for the M-dimensional Bratley test functions.

    Parameters
    ----------
    spatial_dimension : int
        The requested spatial dimension of the probabilistic input model.

    Returns
    -------
    List[UnivDist]
        A list of marginals for the multivariate input following Ref. [1]
    """
    marginals = []
    for i in range(spatial_dimension):
        marginals.append(
            UnivDist(
                name=f"X{i + 1}",
                distribution="uniform",
                parameters=[0.0, 1.0],
                description="None",
            )
        )

    return marginals


AVAILABLE_INPUT_SPECS = {
    "Bratley1992": {
        "name": "Bratley1992",
        "description": (
            "Integration domain of the functions from Bratley et al. (1992)"
        ),
        "marginals": _bratley_input,
        "copulas": None,
    },
}

DEFAULT_INPUT_SELECTION = "Bratley1992"

# The dimension is variable so define a default for fallback
DEFAULT_DIMENSION_SELECTION = 2

# Common metadata used in each class definition of Bratley test functions
COMMON_METADATA = dict(
    _tags=["integration", "sensitivity"],
    _available_inputs=tuple(AVAILABLE_INPUT_SPECS.keys()),
    _available_parameters=None,
    _default_spatial_dimension=None,
    _description="from Bratley et al. (1992)",
)


def _init(
    self,
    spatial_dimension: int = DEFAULT_DIMENSION_SELECTION,
    *,
    prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
    name: Optional[str] = None,
    rng_seed_prob_input: Optional[int] = None,
) -> None:
    """A common __init__ for all Bratley1992 test functions."""
    # --- Arguments processing
    if not isinstance(spatial_dimension, int):
        raise TypeError(
            f"Spatial dimension is expected to be of 'int'. "
            f"Got {type(spatial_dimension)} instead."
        )
    # A Bratley1992 test function is an M-dimensional test function
    # Create the input according to spatial dimension
    prob_input = create_prob_input_from_available(
        prob_input_selection,
        AVAILABLE_INPUT_SPECS,
        spatial_dimension,
        rng_seed_prob_input,
    )
    # Process the default name
    if name is None:
        name = self.__class__.__name__

    UQTestFunABC.__init__(self, prob_input=prob_input, name=name)


class Bratley1992d(UQTestFunABC):
    """A concrete implementation of the function 4 from Bratley et al. (1988).

    Parameters
    ----------
    spatial_dimension : int
        The requested number of spatial_dimension. If not specified,
        the default is set to 2.
    prob_input_selection : str, optional
        The selection of a probabilistic input model from a list of
        available specifications. This is a keyword only parameter.
    name : str, optional
        The name of the instance; if not given the default name is used.
        This is a keyword only parameter.
    rng_seed_prob_input : int, optional
        The seed number for the pseudo-random number generator of the
        corresponding `ProbInput`; if not given `None` is used
        (taken from the system entropy).
        This is a keyword only parameter.
    """

    _tags = COMMON_METADATA["_tags"]
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]
    _default_spatial_dimension = COMMON_METADATA["_default_spatial_dimension"]
    _description = (
        f"Integration test function #4 {COMMON_METADATA['_description']}"
    )

    __init__ = _init  # type: ignore

    def evaluate(self, xx: np.ndarray):
        """Evaluate the test function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            M-Dimensional input values given by an N-by-M array where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the test function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """

        num_points, num_dim = xx.shape
        yy = np.zeros(num_points)

        # Compute the function
        for j in range(num_dim):
            yy += (-1) ** (j + 1) * np.prod(xx[:, : j + 1], axis=1)

        return yy