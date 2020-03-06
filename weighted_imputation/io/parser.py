from .bif import BIF_GRAMMAR
from .dsc import DSC_GRAMMAR
from lark import Lark, tree
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
    parser = Lark(GRAMMARS[ext], parser='lalr', debug=True)
    parsed = parser.parse(text)
    if debug:
        tree.pydot__tree_to_png(parsed, './debug.png')
    parsed = _extract_data(parsed)
    return parsed

def _extract_data(parsed: tree) -> Dict:
    data = {'network': {}, 'nodes': {}, 'values': {}}
    root = parsed.children[0]
    for node in root.children:
        if node.data == 'networkdeclaration':
            pass
        if node.data == 'variabledeclaration':
            key, value = _extract_variable(node.data)
            data['nodes'][key] = value
        if node.data == 'probabilitydeclaration':
            key, value = _extract_probability(node.data)
            data['values'][key] = value
    return data

def _extract_variable(parsed: tree) -> Tuple(str, Dict):
    pass

def _extract_probability(parsed: tree) -> Tuple(str, Dict):
    pass
