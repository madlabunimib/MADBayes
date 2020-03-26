import numpy as np
from .bif import BIF_GRAMMAR
from .dsc import DSC_GRAMMAR
from lark import Lark, Token, tree, Tree, Transformer, Discard
from typing import Dict, Tuple
from os.path import splitext


GRAMMARS = {
    '.bif': BIF_GRAMMAR,
    '.dsc': DSC_GRAMMAR
}

def parse_network_file(path: str, debug=False) -> Dict:
    with open(path, 'r') as file:
        text = file.read()
    _, ext = splitext(path)
    if not ext in GRAMMARS.keys():
        raise Exception('unknown file format.')
    parser = Lark(GRAMMARS[ext], parser='lalr', debug=True)
    parsed = parser.parse(text)
    if debug:
        tree.pydot__tree_to_png(parsed, './debug_0.png')
    parsed = ExtractData(visit_tokens=True).transform(parsed)
    if debug and isinstance(parsed, Tree):
        tree.pydot__tree_to_png(parsed, './debug_1.png')
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
        return Token('levels', [arg.value for arg in args])
    
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
