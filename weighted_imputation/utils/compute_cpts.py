import xarray as xa
import numpy as np
import itertools
from typing import Dict, List


def get_cpts(parsed_file: Dict) -> Dict:
    dictionary = {}
    for key in parsed_file:
        cpt = parsed_file[key]
        
        #Compute dimensions
        dimensions = [key]
        for dim in cpt["dependencies"]:
            dimensions.append(dim)
        
        #Compute coordinates
        coordinates = []
        for node in dimensions:
            coordinates.append(parsed_file[node]["levels"])

        #Compute size of n-d-matrix
        levels = []
        for dim in dimensions:
            levels.append(len(parsed_file[dim]["levels"]))

        data = xa.DataArray(np.zeros(shape=levels), dims=dimensions, coords = coordinates)
        if len(levels) > 1:
            for row in cpt["cpt"]:
                labels = row[0]
                for i, value in enumerate(cpt["levels"]):
                    labels.insert(0, value)
                    data.loc[tuple(labels)] = row[1][i]
                    labels.pop(0)
        else:
            for i, value in enumerate(cpt["levels"]):
                data.loc[value] = cpt["cpt"][0][i]
        
        dictionary.update({key : data})
    return dictionary

def compute_margin_table(node: str, cpts_dict: Dict) -> Dict:
    node_cpt = cpts_dict[node]

    #Compute coordinates
    coordinates = []
    for key in node_cpt.coords[node].values:
        coordinates.append(key)
    
    if not isinstance(node, list):
        node = list(node)
    node_dependencies = [x for x in node_cpt.coords if x not in node]
    dependencies_dict = {}
    for dependencie in node_dependencies:
        dependencies_dict.update({dependencie : []})
        for value in cpts_dict[dependencie].coords[dependencie].values:
            dependencies_dict[dependencie].append(value)

    for coordinate in coordinates:
        for combination in list(_my_product(dependencies_dict)):
            label = [x for x in combination.values()]
            label.insert(0, coordinate)
            for item in combination:                
                node_cpt.loc[tuple(label)] = node_cpt.loc[tuple(label)] * \
                    cpts_dict[item].loc[combination[item]]

    margin_table = xa.DataArray(np.zeros(shape=len(coordinates)), dims=node, coords=[coordinates])
    for coordinate in coordinates:
        margin_table.loc[coordinate] = node_cpt.loc[coordinate].sum()

    return margin_table

def _my_product(input: Dict):
    return (dict(zip(input.keys(), values)) for values in itertools.product(*input.values()))
