import numpy as np
from math import lgamma
from itertools import product

from ..data import load_datasets_from_disk
from ..structures import BayesianNetwork, Dataset
from ..algorithms import parents


def bds_score(dataset: str, bn: BayesianNetwork, iss: float, DEBUG: bool):

    dataset = load_datasets_from_disk()[dataset]
    nodes = bn.nodes()
    nodes_levels = {node: bn.levels(node) for node in nodes}
    
    score = {node : node_bds_score(dataset, bn, iss, nodes_levels, node) for node in nodes}
    if DEBUG:
        from pprint import pprint 
        pprint(score)
    
    return sum(score.values())


def node_bds_score(dataset: Dataset, bn: BayesianNetwork, iss: float, nodes_levels: dict, node) -> float:

    parent_list = parents(bn, node)
    #Create all possible parents configuration
    parents_configurations = dict_product({parent : nodes_levels[parent] for parent in parent_list})
    
    r_i = len(nodes_levels[node])
    q_i = 0
    for parents_conf in parents_configurations:
        if compute_n_ij(dataset, parents_conf) > 0:
            q_i+=1
        
    node_score = 0
    for parents_conf in parents_configurations:
        n_ij = compute_n_ij(dataset, parents_conf)
        a_ijk = compute_a_ijk(iss, n_ij, r_i, q_i)
        a_ij = a_ijk * r_i

        if a_ijk > 0:
            node_score += (lgamma(a_ij) - lgamma(a_ij + n_ij)) #external product/sum
            for level in nodes_levels[node]:
                parents_conf.update({node : level})
                n_ijk = frequencies_count(dataset, parents_conf)                
                node_score += (lgamma(a_ijk+n_ijk) - lgamma(a_ijk)) #inner product/sum

    return node_score

def compute_n_ij(dataset, configuration: dict):
    if configuration != {}:
        return frequencies_count(dataset, configuration)
    else:
        return dataset.get_rows_number()

def compute_a_ijk(iss, n_ij, r_i, q_i):
    if n_ij > 0:
        return iss / (r_i * q_i)
    else:
        return 0

def dict_product(inp):
    return [dict(zip(inp.keys(), values)) for values in product(*inp.values())]

def frequencies_count(dataset, configuration: dict) -> int:

    variables = [variable for variable in configuration]
    configuration_abs_freq = dataset.absolute_frequencies_sublist(variables)

    for _, row in configuration_abs_freq.iterrows():
        match = True
        for variable in variables:
            if not(str(row[variable]) == str(configuration[variable])):
                match = False
                break
        if match:
            return row["count"]
        
    return 0
            