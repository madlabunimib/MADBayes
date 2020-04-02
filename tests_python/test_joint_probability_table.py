import numpy as np
from scipy.stats.contingency import margins
from . import weighted_imputation as wi

def test_joint_probability_table():
    # Generate random jpts from variables count
    variables = list(range(1, 10))
    jpts = [wi.generators.generate_joint_probability_table(n) for n in variables]
    # Compute and flatten margins
    mts = [margins(jpt) for jpt in jpts]
    mts = [[p.flatten().T for p in mt] for mt in mts]
    # Find margins with test function
    jpts = [wi.ProbabilityTable(jpt) for jpt in jpts]
    pts = [
        [jpt.marginalize([dim]).values.astype(float) for dim in jpt.dims]
        for jpt in jpts
    ]
    # Check if jpts have the same margins
    are_equals = [
        all([np.allclose(mts[i][j], pts[i][j]) for j in range(n)])
        for i, n in enumerate(variables)
    ]
    assert(all(are_equals))
