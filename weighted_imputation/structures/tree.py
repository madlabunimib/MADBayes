from typing import Dict, List
from .orderedset import OrderedSet


class Node():

    _label: str
    _parent: "Node"
    _children: OrderedSet
    _attributes: Dict

    def __init__(self, label: str, parent: "Node" = None, children: List = None) -> None:
        self._label = label
        self._parent = parent
        if children is None:
            self._children = OrderedSet()
        else:
            self.set_children(children)
        self._attributes = {}
    
    def __len__(self) -> int:
        return len(self._attributes.keys())

    def __getitem__(self, key) -> Dict:
        return self._attributes[key]

    def __setitem__(self, key, value) -> None:
        self._attributes[key] = value

    def __delitem__(self, key) -> None:
        del(self._attributes[key])

    def __iter__(self):
        return self._attributes.__iter__()
    
    def get_label(self) -> str:
        return self._label
    
    def get_parent(self) -> "Node":
        return self._parent
    
    def set_parent(self, parent: "Node") -> None:
        self._parent = parent
        parent._children.add(self)

    def add_child(self, child: "Node") -> None:
        self._children.add(child)
        child._parent = self
    
    def get_children(self) -> OrderedSet:
        return self._children

    def set_children(self, children: List["Node"]) -> None:
        for child in children:
            self.add_child(child)

    def __eq__(self, other):
        if isinstance(other, "Node"):
            return self._label == other._label
        return NotImplementedError
    
    def __hash__(self):
        return hash(self._label)


class Tree():

    _root: Node
    _nodes: Dict

    def __init__(self, root: Node = None) -> None:
        self._nodes = {}
        if root is None:
            self._root = Node('root')
        else:
            self._root = root
        self._index(self._root)
    
    def __len__(self) -> int:
        return len(self._nodes.keys())

    def __getitem__(self, key) -> Dict:
        if key not in self._nodes.keys():
            self._index(self._root)
        return self._nodes[key]

    def __setitem__(self, key, value) -> None:
        raise NotImplementedError

    def __delitem__(self, key) -> None:
        raise NotImplementedError

    def __iter__(self):
        return self._nodes.__iter__()
    
    def _index(self, node: Node) -> None:
        self._nodes[node.get_label()] = node
        for child in node.get_children():
            self._index(child)
    
    def get_root(self) -> Node:
        return self._root
