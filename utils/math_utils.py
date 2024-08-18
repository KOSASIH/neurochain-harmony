import numpy as np
from scipy.special import erf, erfc
from scipy.optimize import minimize
from sympy import symbols, diff, integrate

class MathUtils:
    def __init__(self):
        pass

    @staticmethod
    def calculate_entropy(values: np.ndarray) -> float:
        """
        Calculate the entropy of a given set of values.

        :param values: The values to calculate the entropy for.
        :return: The entropy of the values.
        """
        probabilities = np.array([value / sum(values) for value in values])
        entropy = -sum([probability * np.log2(probability) for probability in probabilities])
        return entropy

    @staticmethod
    def calculate_gaussian_distribution(mean: float, std_dev: float, x: float) -> float:
        """
        Calculate the probability density function of a Gaussian distribution.

        :param mean: The mean of the Gaussian distribution.
        :param std_dev: The standard deviation of the Gaussian distribution.
        :param x: The value to calculate the probability density for.
        :return: The probability density of the Gaussian distribution at x.
        """
        return np.exp(-((x - mean) ** 2) / (2 * std_dev ** 2)) / (std_dev * np.sqrt(2 * np.pi))

    @staticmethod
    def calculate_erf(x: float) -> float:
        """
        Calculate the error function of a given value.

        :param x: The value to calculate the error function for.
        :return: The error function of x.
        """
        return erf(x)

    @staticmethod
    def calculate_erfc(x: float) -> float:
        """
        Calculate the complementary error function of a given value.

        :param x: The value to calculate the complementary error function for.
        :return: The complementary error function of x.
        """
        return erfc(x)

    @staticmethod
    def optimize_function(func: callable, initial_guess: np.ndarray, bounds: list) -> tuple:
        """
        Optimize a given function using the minimize function from SciPy.

        :param func: The function to optimize.
        :param initial_guess: The initial guess for the optimization.
        :param bounds: The bounds for the optimization.
        :return: The optimized parameters and the minimum value of the function.
        """
        result = minimize(func, initial_guess, method="SLSQP", bounds=bounds)
        return result.x, result.fun

    @staticmethod
    def calculate_derivative(func: callable, x: float, h: float = 1e-7) -> float:
        """
        Calculate the derivative of a given function using the definition of a derivative.

        :param func: The function to calculate the derivative for.
        :param x: The value to calculate the derivative at.
        :param h: The step size for the derivative calculation.
        :return: The derivative of the function at x.
        """
        return (func(x + h) - func(x - h)) / (2 * h)

    @staticmethod
    def calculate_integral(func: callable, a: float, b: float, num_points: int = 1000) -> float:
        """
        Calculate the integral of a given function using the trapezoidal rule.

        :param func: The function to calculate the integral for.
        :param a: The lower bound of the integral.
        :param b: The upper bound of the integral.
        :param num_points: The number of points to use for the integral calculation.
        :return: The integral of the function from a to b.
        """
        x = np.linspace(a, b, num_points)
        y = func(x)
        return np.trapz(y, x)

    @staticmethod
    def calculate_symbolic_derivative(func: str, var: str) -> str:
        """
        Calculate the symbolic derivative of a given function using SymPy.

        :param func: The function to calculate the derivative for.
        :param var: The variable to calculate the derivative with respect to.
        :return: The symbolic derivative of the function.
        """
        x = symbols(var)
        func = sympify(func)
        return str(diff(func, x))

    @staticmethod
    def calculate_symbolic_integral(func: str, var: str) -> str:
        """
        Calculate the symbolic integral of a given function using SymPy.

        :param func: The function to calculate the integral for.
        :param var: The variable to calculate the integral with respect to.
        :return: The symbolic integral of the function.
        """
        x = symbols(var)
        func = sympify(func)
        return str(integrate(func, x))
