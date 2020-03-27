from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import xarray as xa

from ..io import parse_network_file
from .conditional_probability_table import ConditionalProbabilityTable
from .graph import DirectedGraph
from .joint_probability_table import JointProbabilityTable
from .probability_table import ProbabilityTable


class BayesianNetwork(DirectedGraph):

    def __init__(self, nodes: List[str] = None, adjacency_matrix: np.ndarray = None, cpts: Dict = None) -> None:
        super().__init__(nodes, adjacency_matrix)
        if cpts is not None:
            self.set_cpts(cpts)
    
    def set_cpts(self, cpts: Dict) -> None:
        if set(self.nodes()) != set(cpts.keys()):
            raise Exception('cpts must contain all and only nodes CPTS.')
        for node, cpt in cpts.items():
            self[node]['CPT'] = cpt
        self._compute_margin_tables()
    
    def _compute_margin_tables(self) -> None:
        for node in self.nodes():
            self._compute_pt(node)
    
    def _compute_pt(self, node: str) -> None:
        attributes = self[node]
        if 'PT' not in attributes:
            self._compute_jpt(node)
            attributes['PT'] = attributes['JPT'].marginalize([node])
    
    def _compute_jpt(self, node: str) -> None:
        attributes = self[node]
        if 'JPT' not in attributes:
            cpt = attributes['CPT']
            jpt = JointProbabilityTable.from_probability_table(cpt)
            parents = cpt.dependencies()
            if len(parents) > 0:
                for parent in parents:
                    self._compute_pt(parent)
                for location in cpt.locations():
                    for parent in parents:
                        pt = self[parent]['PT']
                        # TODO: Find a way to remove the medium pointer
                        pointer = tuple([*location.values()])
                        jpt.loc[pointer] = jpt(**location) * pt(**location)
            attributes['JPT'] = jpt
    
    @classmethod
    def _structure_from_file_parsed(cls, parsed: Dict) -> Tuple:
        n = len(parsed.keys())
        nodes = list(parsed.keys())
        adjacency_matrix = np.zeros((n, n), dtype=bool)
        for key, value in parsed.items():
            child = nodes.index(key)
            for dependency in value['dependencies']:
                parent = nodes.index(dependency)
                adjacency_matrix[parent, child] = True
        return nodes, adjacency_matrix
    
    @classmethod
    def _cpts_from_file_parsed(cls, parsed: Dict) -> Dict:
        cpts = {}
        for node, value in parsed.items():
            nodes = [node] + value['dependencies']
            levels = [parsed[node]['levels'] for node in nodes]
            if len(value['dependencies']) == 0:
                data = [
                    ([i], v)
                    for i, v in enumerate(value['cpt'][0])
                ]
            else:
                data = [
                    ([i] + [levels[j+1].index(w)
                            for j, w in enumerate(row[0])], v)
                    for row in value['cpt']
                    for i, v in enumerate(row[1])
                ]
            data = [(tuple(location), item) for location, item in data]
            cpt = np.zeros([len(l) for l in levels])
            for (location, item) in data:
                cpt[location] = item
            cpts[node] = ConditionalProbabilityTable.from_data(cpt, nodes, levels)
        return cpts

    @classmethod
    def from_file(cls, path: str) -> None:
        parsed = parse_network_file(path)
        nodes , adjacency_matrix = cls._structure_from_file_parsed(parsed)
        cpts = cls._cpts_from_file_parsed(parsed)
        return cls(nodes, adjacency_matrix, cpts)
