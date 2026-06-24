"""
EABC-Qubit: Quantenmechanisches Framework für topologische Primzahldefekte

Ein vollwertiges numerisches Framework zur Untersuchung der spektralen Eigenschaften
eines eindimensionalen Quantensystems mit internem Freiheitsgrad (Chiralität) und
topologischen Defekten an Primzahlpositionen.
"""

__version__ = "0.1.0"
__author__ = "Thomas Hoffbauer"

from .primes import generate_primes, eabc_classification
from .hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
from .spectral import compute_spectrum, spectral_unfolding
from .level_spacing import compute_level_spacing, fit_level_statistics
from .visualization import (
    plot_level_statistics,
    plot_eigenspectrum,
    plot_parameter_sweep
)
from .collatz_weights import (
    collatz_log_rate,
    collatz_log_rate_prime,
    collatz_weights_array,
    random_soup_weights
)

__all__ = [
    "generate_primes",
    "eabc_classification",
    "EABCHamiltonian",
    "CollatzEABCHamiltonian",
    "compute_spectrum",
    "spectral_unfolding",
    "compute_level_spacing",
    "fit_level_statistics",
    "plot_level_statistics",
    "plot_eigenspectrum",
    "plot_parameter_sweep",
    "collatz_log_rate",
    "collatz_log_rate_prime",
    "collatz_weights_array",
    "random_soup_weights",
]
