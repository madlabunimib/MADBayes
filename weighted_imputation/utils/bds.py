import numpy as np
from math import lgamma
from itertools import product

from ..data import load_datasets_from_disk
from ..structures import BayesianNetwork
from ..algorithms import parents

def bds_score(dataset: str, bn: BayesianNetwork, iss: float):

    dataset = load_datasets_from_disk()[dataset]
    abs_freq = dataset.absolute_frequencies()
    
    score = 0

    nodes = bn.nodes()
    node_levels = {}
    #nodes -> ['A', 'S', 'E', 'O', 'R', 'T']
    for node in nodes:
        node_levels.update({node: bn.levels(node)})

    '''first product'''
    for node in nodes:
        parent_list = parents(bn, node)
        if len(parent_list) > 0:
            #Create all possible parents configuration
            parents_configurations = dict_product({par : node_levels[par] for par in parent_list})

            r_i = len(node_levels[node])
            q_i = len(parents_configurations)

            '''second product'''
            for parents_conf in parents_configurations:
                n_ij = configuration_count(dataset, parents_conf)
                a_ij = 0

                '''third product'''
                for level in node_levels[node]:
                    parents_conf.update({node : level})
                    n_ijk = configuration_count(dataset, parents_conf)
                    a_ijk = compute_iss_ijk(iss, n_ij, r_i, q_i)
                    score += (lgamma(a_ijk+n_ijk) / lgamma(a_ijk))
                    
                    a_ij += a_ijk #Sum over k to obtain a_ij

                score += (lgamma(a_ij) / lgamma(a_ij + n_ij))
    return score


def compute_iss_ijk(iss, n_ij, r_i, q_i):
    if n_ij > 0:
        return iss / (r_i * q_i)
    else:
        return 0

def dict_product(inp):
    return [dict(zip(inp.keys(), values)) for values in product(*inp.values())]

def configuration_count(dataset, configuration: dict) -> int:

    variables = [variable for variable in configuration]
    configuration_abs_freq = dataset.absolute_frequencies_sublist(variables)

    for _, row in configuration_abs_freq.iterrows():
        match = True
        for variable in variables:
            if not(row[variable] == configuration[variable]):
                match = False
                break
        if match:
            return row["count"]
        
    return 0
            