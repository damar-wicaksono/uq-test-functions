"""
Module with an implementation of the McLain's test functions.

The McLain's test functions consists of five two-dimensional scalar-valued
functions. The functions were introduced in [1] in the context of drawing
contours from a given set of points.

There are five test functions in McLain's paper each models a mathematically
defined surface:

- S1: A part of a sphere
- S2: A steep hill rising from a plain
- S3: A less steep hill
- S4: A long narrow hill
- S5: A plateau and plain separated by a steep cliff

Four of the functions (S1-S3 and S5) appeared in modified forms in [2].

References
----------

1. D. H. McLain, "Drawing contours from arbitrary data points," The Computer
   Journal, vol. 17, no. 4, pp. 318-324, 1974.
   DOI: 10.1093/comjnl/17.4.318
2. Richard Franke, "A critical comparison of some methods for interpolation
   of scattered data," Naval Postgraduate School, Monterey, Canada,
   Technical Report No. NPS53-79-003, 1979.
   URL: https://core.ac.uk/reader/36727660
"""
import numpy as np

from typing import Optional

from ..core.prob_input.input_spec import MarginalSpec, ProbInputSpec
from ..core.uqtestfun_abc import UQTestFunABC
from .available import get_prob_input_spec, create_prob_input_from_spec

__all__ = ["McLainS1", "McLainS2", "McLainS3", "McLainS4", "McLainS5"]

INPUT_MARGINALS_MCLAIN1974 = [  # From Ref. [1]
    MarginalSpec(
        name="X1",
        distribution="uniform",
        parameters=[1.0, 10.0],
        description="None",
    ),
    MarginalSpec(
        name="X2",
        distribution="uniform",
        parameters=[1.0, 10.0],
        description="None",
    ),
]

AVAILABLE_INPUT_SPECS = {
    "McLain1974": ProbInputSpec(
        name="McLain-1974",
        description=(
            "Input specification for the McLain's test functions "
            "from McLain (1974)."
        ),
        marginals=INPUT_MARGINALS_MCLAIN1974,
        copulas=None,
    ),
}

DEFAULT_INPUT_SELECTION = "McLain1974"

COMMON_METADATA = dict(
    _tags=["metamodeling"],
    _available_inputs=tuple(AVAILABLE_INPUT_SPECS.keys()),
    _available_parameters=None,
    _default_spatial_dimension=2,
    _description="from McLain (1974)",
)


def _init(
    self,
    *,
    prob_input_selection: Optional[str] = DEFAULT_INPUT_SELECTION,
    name: Optional[str] = None,
    rng_seed_prob_input: Optional[int] = None,
) -> None:
    """A common __init__ for all McLain's test functions."""
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

    UQTestFunABC.__init__(self, prob_input=prob_input, name=name)


class McLainS1(UQTestFunABC):
    """A concrete implementation of the McLain S1 function.

    The function features a part of a sphere.
    """

    _tags = COMMON_METADATA["_tags"]
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]
    _default_spatial_dimension = COMMON_METADATA["_default_spatial_dimension"]
    _description = f"McLain S1 function {COMMON_METADATA['_description']}"

    __init__ = _init  # type: ignore

    def evaluate(self, xx: np.ndarray):
        """Evaluate the McLain S1 function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            Two-Dimensional input values given by N-by-2 arrays where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the McLain S1 function evaluated
            on the input values.
            The output is a 1-dimensional array of length N.
        """
        yy = np.sqrt(64 - (xx[:, 0] - 5.5) ** 2 - (xx[:, 1] - 5.5) ** 2)

        return yy


class McLainS2(UQTestFunABC):
    """A concrete implementation of the McLain S2 function.

    The function features a steep hill rising from a plain.
    """

    _tags = COMMON_METADATA["_tags"]
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]
    _default_spatial_dimension = COMMON_METADATA["_default_spatial_dimension"]
    _description = f"McLain S2 function {COMMON_METADATA['_description']}"

    __init__ = _init  # type: ignore

    def evaluate(self, xx: np.ndarray):
        """Evaluate the McLain S2 function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            Two-Dimensional input values given by N-by-2 arrays where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the McLain S2 function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """
        yy = np.exp(-1.0 * ((xx[:, 0] - 5) ** 2 + (xx[:, 1] - 5) ** 2))

        return yy


class McLainS3(UQTestFunABC):
    """A concrete implementation of the McLain S3 function.

    The function features a less steep hill (compared to S2).
    """

    _tags = COMMON_METADATA["_tags"]
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]
    _default_spatial_dimension = COMMON_METADATA["_default_spatial_dimension"]
    _description = f"McLain S3 function {COMMON_METADATA['_description']}"

    __init__ = _init  # type: ignore

    def evaluate(self, xx: np.ndarray):
        """Evaluate the McLain S3 function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            Two-Dimensional input values given by N-by-2 arrays where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the McLain S3 function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """
        yy = np.exp(-0.25 * ((xx[:, 0] - 5) ** 2 + (xx[:, 1] - 5) ** 2))

        return yy


class McLainS4(UQTestFunABC):
    """A concrete implementation of the McLain S4 function.

    The function features a long narrow hill.
    """

    _tags = COMMON_METADATA["_tags"]
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]
    _default_spatial_dimension = COMMON_METADATA["_default_spatial_dimension"]
    _description = f"McLain S4 function {COMMON_METADATA['_description']}"

    __init__ = _init  # type: ignore

    def evaluate(self, xx: np.ndarray):
        """Evaluate the McLain S4 function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            Two-Dimensional input values given by N-by-2 arrays where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the McLain S4 function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """
        yy = np.exp(
            -1
            * (
                (xx[:, 0] + xx[:, 1] - 11) ** 2
                + (xx[:, 0] - xx[:, 1]) ** 2 / 10.0
            )
        )

        return yy


class McLainS5(UQTestFunABC):
    """A concrete implementation of the McLain S5 function.

    The function features two plateaus separated by a steep cliff.
    """

    _tags = COMMON_METADATA["_tags"]
    _available_inputs = COMMON_METADATA["_available_inputs"]
    _available_parameters = COMMON_METADATA["_available_parameters"]
    _default_spatial_dimension = COMMON_METADATA["_default_spatial_dimension"]
    _description = f"McLain S5 function {COMMON_METADATA['_description']}"

    __init__ = _init  # type: ignore

    def evaluate(self, xx: np.ndarray):
        """Evaluate the McLain S5 function on a set of input values.

        Parameters
        ----------
        xx : np.ndarray
            Two-Dimensional input values given by N-by-2 arrays where
            N is the number of input values.

        Returns
        -------
        np.ndarray
            The output of the McLain S5 function evaluated on the input values.
            The output is a 1-dimensional array of length N.
        """
        yy = np.tanh(xx[:, 0] + xx[:, 1] - 11)

        return yy
