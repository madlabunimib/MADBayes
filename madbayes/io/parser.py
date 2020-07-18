import numpy as np
import xarray as xa
from .bif import BIF_GRAMMAR
from .dsc import DSC_GRAMMAR
from lark import Lark, Token, tree, Tree, Transformer, Discard
from typing import Dict, Tuple
from os.path import splitext


GRAMMARS = {
    '.bif': BIF_GRAMMAR,
    '.dsc': DSC_GRAMMAR
}


def parse_network_file(path: str) -> Dict:
    with open(path, 'r') as file:
        text = file.read()
    _, ext = splitext(path)
    if not ext in GRAMMARS.keys():
        raise Exception('unknown file format.')
    parser = Lark(GRAMMARS[ext], parser='lalr', debug=True)
    parsed = parser.parse(text)
    parsed = ExtractData(visit_tokens=True).transform(parsed)
    return parsed


class ExtractData(Transformer):

    def VARIABLE(self, args):
        raise Discard

    def VARIABLETYPE(self, args):
        raise Discard

    def DISCRETE(self, args):
        raise Discard

    def DECIMAL_LITERAL(self, args):
        raise Discard

    def PROBABILITY(self, args):
        raise Discard

    def TABLEVALUES(self, args):
        raise Discard

    def networkdeclaration(self, args):
        raise Discard

    def probabilityvariablevalue(self, args):
        return args[0]

    def variablevalueslist(self, args):
        return Token('levels', [arg.value for arg in args])

    def variablediscrete(self, args):
        return args[0]

    def variablecontent(self, args):
        return args[0]

    def probabilityvariablename(self, args):
        return Token('label', args[0].value)

    def variabledeclaration(self, args):
        return Token('variabledeclaration', {arg.type: arg.value for arg in args})

    def probabilityvalueslist(self, args):
        return Token('levels', [str(arg.value) for arg in args])

    def floatingpointlist(self, args):
        return Token('probability', [float(arg.value) for arg in args])

    def probabilitytable(self, args):
        return Token('table', args[0].value)

    def probabilityentry(self, args):
        return Token('table', [args[0].value, args[1].value])

    def probabilitycontent(self, args):
        return Token('table', [arg.value for arg in args])

    def probabilityvariableslist(self, args):
        return Token('labels', [arg.value for arg in args])

    def probabilitydeclaration(self, args):
        return Token('probabilitydeclaration', {arg.type: arg.value for arg in args})

    def compilationunit(self, args):
        variables = {
            arg.value['label']: {'levels': arg.value['levels']}
            for arg in args
            if arg.type == 'variabledeclaration'
        }
        probabilities = {
            arg.value['labels'][0]: {
                'dependencies': arg.value['labels'][1:],
                'cpt': arg.value['table']
            }
            for arg in args
            if arg.type == 'probabilitydeclaration'
        }
        for key, value in probabilities.items():
            variables[key].update(value)
        return Token('parsed', variables)

    def start(self, args):
        return args[0].value


def bayesian_network_from_file(path: str) -> Tuple:
    with open(path, 'r') as file:
        text = file.read()
    _, ext = splitext(path)
    if not ext in GRAMMARS.keys():
        raise Exception('Unknown file format.')
    parser = Lark(GRAMMARS[ext], parser='lalr', debug=True)
    parsed = parser.parse(text)
    parsed = ExtractData(visit_tokens=True).transform(parsed)
    nodes = list(parsed.keys())
    edges = [
        (parent, child)
        for child, attr in parsed.items()
        for parent in attr['dependencies']
    ]
    cpts = {}
    for node, attr in parsed.items():
        variables = [node] + attr['dependencies']
        levels = [parsed[node]['levels'] for variable in variables]
        if len(attr['dependencies']) == 0:
            data = [
                ([i], v)
                for i, v in enumerate(attr['cpt'][0])
            ]
        else:
            data = [
                ([i] + [levels[j + 1].index(w)
                        for j, w in enumerate(row[0])], v)
                for row in attr['cpt']
                for i, v in enumerate(row[1])
            ]
        data = [(tuple(location), item) for location, item in data]
        cpt = np.zeros([len(l) for l in levels])
        for (location, item) in data:
            cpt[location] = item
        cpts[node] = xa.DataArray(data=cpt, dims=variables, coords=levels)
    return nodes, edges, cpts


@classmethod
def from_file(cls, path: str) -> None:
    nodes, edges, cpts = bayesian_network_from_file(path)
    bayesian_network = cls(nodes, cpts)
    for (parent, child) in edges:
        bayesian_network.add_edge(parent, child)
    return bayesian_network
