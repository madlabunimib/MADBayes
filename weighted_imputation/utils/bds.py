from math import gamma
from itertools import product

from ..data import load_datasets_from_disk
from ..structures import BayesianNetwork
from ..algorithms import parents

def bds_score(dataset: str, bn: BayesianNetwork, iss: float):

    dataset = load_datasets_from_disk()[dataset]
    abs_freq = dataset.absolute_frequencies()
    
    nodes = bn.nodes()
    node_levels = {}
    #nodes -> ['A', 'S', 'E', 'O', 'R', 'T']
    for node in nodes:
        node_levels.update({node: bn.levels(node)})

    
    '''first product'''
    for node in nodes:
        parent_list = parents(bn, node)
        #Create all possible parents configuration
        parents_configurations = dict_product({par : node_levels[par] for par in parent_list})
        
        '''second product''' #for every parent configuration 
        for parents_conf in parents_configurations:
            parent_node_configuration = parents_conf
            
            '''third product''' #Add every level of node to every parent configuration
            for level in node_levels[node]:
                parent_node_configuration.update({node : level})






        #if parent_list != []:
        #    parent_abs_freq = dataset.absolute_frequencies_sublist(parent_list)

    return 


def compute_iss_ijk(iss, n_ij, r_i, q_i):
    if n_ij > 0:
        return iss / (r_i * q_i)
    else:
        return 0

def dict_product(inp):
    return (dict(zip(inp.keys(), values)) for values in product(*inp.values()))
