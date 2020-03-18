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
