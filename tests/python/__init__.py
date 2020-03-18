import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import weighted_imputation
from weighted_imputation import disable_alternative_backend

# Set Pure Python testing
disable_alternative_backend()