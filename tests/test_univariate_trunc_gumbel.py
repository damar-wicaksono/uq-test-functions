"""
Test module for UnivariateInput instances with a truncated Gumbel (max.) dist.
"""
import pytest
import numpy as np
import scipy.integrate as integrate

from scipy.stats import gumbel_r

from uqtestfuns.core.prob_input.univariate_input import UnivariateInput
from uqtestfuns.global_settings import ARRAY_FLOAT
from conftest import create_random_alphanumeric


DISTRIBUTION_NAME = "trunc-gumbel"


def _calc_median(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical median of a given trunc. Gumbel (max.) dist."""
    mu, beta, lb, ub = parameters[:]

    lb_quantile = gumbel_r.cdf(lb, loc=mu, scale=beta)
    ub_quantile = gumbel_r.cdf(ub, loc=mu, scale=beta)

    median = gumbel_r.ppf(
        (lb_quantile + ub_quantile) / 2.0, loc=mu, scale=beta
    )

    return float(median)


def _calc_mode(parameters: ARRAY_FLOAT) -> float:
    """Compute the analytical mode of a Gumbel (max.) distribution."""
    mu, _, _, _ = parameters[:]

    return mu


def _calc_mean(parameters: ARRAY_FLOAT) -> float:
    """Compute the mean of a truncated Gumbel (max.) distribution.

    Notes
    -----
    - The computation is carried via numerical integration.
    """
    mu, beta, lb, ub = parameters[:]

    def _integrand(x):
        return gumbel_r.pdf(x, loc=mu, scale=beta) * x

    lb_quantile = gumbel_r.cdf(lb, loc=mu, scale=beta)
    ub_quantile = gumbel_r.cdf(ub, loc=mu, scale=beta)
    normalizing_factor = ub_quantile - lb_quantile

    mean = integrate.quad(_integrand, lb, ub)[0] / normalizing_factor

    return mean


def test_wrong_number_of_parameters() -> None:
    """Test the failure of specifying wrong number of parameters."""
    name = create_random_alphanumeric(5)
    distribution = DISTRIBUTION_NAME
    # Gumbel distribution expects 4 parameters not 5!
    parameters = np.sort(np.random.rand(5))

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_failed_parameter_verification() -> None:
    """Test the failure of specifying invalid parameter values."""
    name = create_random_alphanumeric(10)
    distribution = DISTRIBUTION_NAME
    # The 2nd parameter of the Gumbel (max.) dist. must be strictly positive!
    parameters = [7.71, -5.0, 0, 10]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The 1st parameter of the Gumbel (max.) dist. must be within the bounds!
    parameters = [7.71, 0.5, 0, 5]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )

    # The lower bound is larger than the upper bound!
    parameters = [2.71, 0.5, 5, 0]

    with pytest.raises(ValueError):
        UnivariateInput(
            name=name, distribution=distribution, parameters=parameters
        )


def test_estimate_mode() -> None:
    """Test the mode estimation of a Gumbel (max.) distribution."""
    # Create a set of random parameters
    parameters = np.sort(1 + 5 * np.random.rand(3))
    parameters[[0, 1]] = parameters[[1, 0]]
    # Insert beta as the second parameter
    parameters = np.insert(parameters, 1, np.random.rand(1))

    # Create an instance
    my_univariate_input = UnivariateInput(
        distribution=DISTRIBUTION_NAME, parameters=parameters
    )

    # Generate a sample
    sample_size = 1000000  # Should give 1e-0 accuracy
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    y, edges = np.histogram(xx, bins="auto")
    mode = edges[np.argmax(y)]

    # Analytical result
    mode_ref = _calc_mode(parameters)

    # Assertion
    assert np.isclose(mode, mode_ref, rtol=1, atol=1)


def test_estimate_median() -> None:
    """Test the median estimation of a Gumbel (max.) distribution."""
    # Create a set of random parameters
    parameters = np.sort(1 + 5 * np.random.rand(3))
    parameters[[0, 1]] = parameters[[1, 0]]
    # Insert beta as the second parameter
    parameters = np.insert(parameters, 1, np.random.rand(1))

    # Create an instance
    my_univariate_input = UnivariateInput(
        distribution=DISTRIBUTION_NAME, parameters=parameters
    )

    # Generate a sample
    sample_size = 100000  # Should give 1e-2 accuracy
    xx = my_univariate_input.get_sample(sample_size)

    # Estimated result
    median = np.median(xx)

    # Analytical result
    median_ref = _calc_median(parameters)

    # Assertion
    assert np.isclose(median, median_ref, rtol=1e-2, atol=1e-2)
