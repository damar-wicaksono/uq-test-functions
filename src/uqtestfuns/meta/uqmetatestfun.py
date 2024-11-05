"""
This module contains the implementation of the meta in UQTestFuns.

The implementation is based on the meta proposed in [1].
To further specify the meta, a set of default parameter values
according to [1] is also implemented.

References
----------

1. William Becker, “Metafunctions for benchmarking in sensitivity analysis,”
   Reliability Engineering & System Safety, vol. 204, p. 107189, 2020,
   doi:
   `10.1016/j.ress.2020.107189 <https://doi.org/10.1016/j.ress.2020.107189>`_.
"""

import math
import numpy as np

from dataclasses import dataclass
from numpy.typing import ArrayLike
from typing import Optional, Union, List

from uqtestfuns.core.parameters import FunParams
from .metaspec import UQMetaFunSpec, UQTestFunSpec
from .basis_functions import BASIS_BY_ID
from ..core import UQTestFun, ProbInput, Marginal


__all__ = ["UQMetaTestFun", "default_coeffs_gen"]


def default_coeffs_gen(sample_size: int) -> np.ndarray:
    r"""Generate coefficient values for each effect term using the default.

    The default coefficient values generator is a Gaussian mixture distribution
    as proposed in [1] with the following form:

    .. math::
       \mathcal{GM}(\phi, \mu_1, \sigma_1, \mu_2, \sigma_2) =
       \phi \mathcal{N}(\mu_1, \sigma_1)
       + (1 - \phi) \mathcal{N}(\mu_2, \sigma_2)

    where :math:`\phi = 0.7`, :math:`\mu_1 = 0`, :math:`\mu_2 = 0`,
    :math:`\sigma_1 = \sqrt{0.5}`, and :math:`\sigma_2 = \sqrt{5}`.

    Parameters
    ----------
    sample_size : int
        Number of sample points to generate.

    Returns
    -------
    np.ndarray
        The coefficient values generated by the generator.
    """
    yy = np.zeros(sample_size)

    phi = 0.7
    sigma_1 = np.sqrt(0.5)
    sigma_2 = np.sqrt(5)

    choices = np.random.choice([0, 1], p=[phi, 1 - phi], size=sample_size)
    yy[choices == 0] = np.random.normal(0, sigma_1, size=np.sum(choices == 0))
    yy[choices == 1] = np.random.normal(0, sigma_2, size=np.sum(choices == 1))

    return yy


def _evaluate_test_function(xx: np.ndarray, spec: UQTestFunSpec) -> np.ndarray:
    """Alternative way to evaluate metafunction realizations."""

    basis_functions = spec.basis_functions
    selected_basis = spec.selected_basis

    # Evaluate the selected basis functions on xx
    basis_vals = np.zeros((xx.shape[0], spec.input_dimension))
    for idx, basis_id in enumerate(selected_basis):
        basis_vals[:, idx] = basis_functions[basis_id](xx[:, idx])

    effects_tuples = spec.effects_tuples
    effects_coeffs = spec.effects_coeffs

    # Evaluate each effect term of the test function
    yy = np.zeros(xx.shape[0])
    for key in effects_tuples:
        n_way = effects_tuples[key]
        coeffs = effects_coeffs[key]

        for dim_indices, coeff in zip(n_way, coeffs):
            yy[:] += coeff * np.prod(basis_vals[:, dim_indices], axis=1)

    return yy


@dataclass
class UQMetaTestFun:
    """Implementation of the metafunction.

    A metafunction is a test-function-generating function.
    A random realization of a test function can be generated
    from a metafunction.

    Parameters
    ----------
    metafun_spec : UQMetaFunSpec
        An instance of meta specification that fully defines a
        meta.
    """

    metafun_spec: UQMetaFunSpec

    def get_sample(
        self, sample_size=1
    ) -> Optional[Union[UQTestFun, List[UQTestFun]]]:
        """Generate realizations of test function.

        Parameters
        ----------
        sample_size : int
            Number of test function realizations.

        Returns
        -------
        Optional[Union[UQTestFun, List[UQTestFun]]]
            Realization(s) of UQTestFunSpec.

        Notes
        -----
        - With sample_size larger than one, a list of UQTestFun instances
          is returned.
        """
        if sample_size < 1:
            return None

        # Generate realizations of test function specification
        testfun_specs = self.metafun_spec.get_sample(sample_size)

        # Create the name
        name = "metafunction_realization"
        # Create the evaluation callable
        evaluate = _evaluate_test_function

        if sample_size == 1:
            assert testfun_specs is not None
            assert not isinstance(testfun_specs, list)
            # Create an instance of inputs
            prob_input = ProbInput(testfun_specs.inputs)
            # Assign the realized spec as a parameter
            parameters = FunParams(
                declared_parameters=[
                    {
                        "keyword": "spec",
                        "value": testfun_specs,
                        "type": UQTestFunSpec,
                    },
                ],
            )

            return UQTestFun(
                evaluate=evaluate,
                prob_input=prob_input,
                parameters=parameters,
                function_id=name,
            )

        sample = []
        for i in range(sample_size):
            # Create an instance of inputs
            assert isinstance(testfun_specs, list)
            prob_input = ProbInput(testfun_specs[i].inputs)
            # Assign the realized spec as a parameter
            parameters = FunParams(
                declared_parameters=[
                    {
                        "keyword": "spec",
                        "value": testfun_specs[i],
                        "type": UQTestFunSpec,
                    },
                ],
            )

            sample.append(
                UQTestFun(
                    evaluate=evaluate,
                    prob_input=prob_input,
                    parameters=parameters,
                    function_id=name,
                )
            )

        return sample

    @classmethod
    def from_default(
        cls,
        input_dimension: ArrayLike,
        input_id: Optional[int] = None,
    ):
        """Create a metafunction with parameters according to Becker (2019).

        Parameters
        ----------
        input_dimension : Union[int, Sized]
            Number of dimensions of the test functions generated
            by the meta. If a set of values are given, a single value
            will be selected at random.

        Returns
        -------
        UQMetaTestFun
            An instance of metafunction with the default parameters.
        """
        # Select a single input dimension randomly
        if not isinstance(input_dimension, int):
            input_dimension = np.asarray(input_dimension)
            input_dimension = int(np.random.choice(input_dimension))

        effects_dict = {
            1: None,  # Take all
            2: math.floor(0.5 * input_dimension),
            3: math.floor(0.2 * input_dimension),
        }

        if input_id is None:
            input_id = np.random.randint(0, 8)

        input_marginals = [
            Marginal(distribution="uniform", parameters=[0, 1]),
            Marginal(
                distribution="trunc-normal",
                parameters=[0.5, 0.15, 0.0, 1.0],
            ),
            Marginal(distribution="beta", parameters=[8.0, 2.0, 0.0, 1.0]),
            Marginal(distribution="beta", parameters=[2.0, 8.0, 0.0, 1.0]),
            Marginal(distribution="beta", parameters=[2.0, 0.8, 0.0, 1.0]),
            Marginal(distribution="beta", parameters=[0.8, 2.0, 0.0, 1.0]),
            Marginal(distribution="logitnormal", parameters=[0.0, 3.16]),
        ]

        if input_id < 7:
            input_marginals = [input_marginals[input_id]]

        metafun_spec = UQMetaFunSpec(
            input_dimension=input_dimension,
            basis_functions=BASIS_BY_ID,
            effects_dict=effects_dict,
            input_marginals=input_marginals,
            coeffs_generator=default_coeffs_gen,
        )

        return cls(metafun_spec)
