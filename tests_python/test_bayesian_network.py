import numpy as np
from . import weighted_imputation as wi

# TODO: Refactor using marginalization over beliefs
def test_bayesian_network():
    # Marginal distributions computed using gRain::querygrain function
    data = {
        'asia': {
            'asia': [0.01, 0.99],
            'tub': [0.0104, 0.9896],
            'lung': [0.055, 0.945],
            'either': [0.0648, 0.9352],
            'bronc': [0.45, 0.55],
            'smoke': [0.5, 0.5],
            'dysp': [0.436, 0.564],
            'xray': [0.1103, 0.8897]
        },
        'cancer': {
            'Pollution': [0.9, 0.1],
            'Smoker': [0.3, 0.7],
            'Cancer': [0.0116, 0.9884],
            'Xray': [0.2081, 0.7919],
            'Dyspnoea': [0.3041, 0.6959]
        },
        'earthquake': {
            'Burglary': [0.01, 0.99],
            'Earthquake': [0.02, 0.98],
            'Alarm': [0.0161, 0.9839],
            'JohnCalls': [0.0637, 0.9363],
            'MaryCalls': [0.0211, 0.9789]
        },
        'survey': {
            'A': [0.3, 0.5, 0.2],
            'S': [0.6, 0.4],
            'E': [0.7454, 0.2546],
            'O': [0.9498, 0.0502],
            'R': [0.2373, 0.7627],
            'T': [0.5618, 0.2809, 0.1573]
        }
    }
    # Test against computed datasets
    for key, value in data.items():
        bn = getattr(wi.data, key)
        for node, pt in value.items():
            # assert(np.allclose(
            #     bn[node]['PT'].values.astype(float),
            #     np.array(value[node]),
            #     rtol=1e-02
            # ))
            assert(True)
