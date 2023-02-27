"""
Utility module for all the UQ test functions.
"""
from .prob_input.univariate_distribution import UnivDist
from .prob_input.probabilistic_input import ProbInput


def create_canonical_uniform_input(
    spatial_dimension: int, min_value: float, max_value: float
) -> ProbInput:
    """Create a MultivariateInput in a canonical domain of [-1, 1]^M.

    Parameters
    ----------
    spatial_dimension : int
        The requested number of dimension.
    min_value : float, optional
        The minimum value of the domain.
    max_value : float, optional
        The maximum value of the domain.

    Returns
    -------
    ProbInput
        The M-dimensional MultivariateInput with independent marginals each
        on [min_value, max_value].
    """

    marginals = []

    for i in range(spatial_dimension):
        marginals.append(
            UnivDist(
                name=f"X{i+1}",
                distribution="uniform",
                parameters=[min_value, max_value],
            )
        )

    return ProbInput(marginals)
