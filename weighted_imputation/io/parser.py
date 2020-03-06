from .bif import BIF_GRAMMAR
from .dsc import DSC_GRAMMAR
from lark import Lark, tree
from os.path import splitext


GRAMMARS = {
    '.bif': BIF_GRAMMAR,
    '.dsc': DSC_GRAMMAR
}

def parse_network_file(path: str, debug=False):
    with open(path, 'r') as file:
        text = file.read()
    _, ext = splitext(path)
    parser = Lark(GRAMMARS[ext], parser='lalr', debug=True)
    parsed = parser.parse(text)
    if debug:
        tree.pydot__tree_to_png(parsed, './debug.png')
    return parsed
