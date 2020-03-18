import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import weighted_imputation
from weighted_imputation import set_alternative_backend

# Set Numba backend testing
set_alternative_backend('numba')