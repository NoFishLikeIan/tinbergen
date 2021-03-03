import numpy as np

from typing import NewType, Tuple, Dict, Optional

from statistics.tests import TestResult

Tests = NewType("Tests", Dict[str, TestResult])

EstimationResults = NewType(
    "EstimationResults",
    Tuple[
        np.ndarray, 
        np.ndarray, 
        np.ndarray,
        np.ndarray, 
        Optional[Tests]
    ]
)
