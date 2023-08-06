
class Node:
    def __init__(self, data, parent=None):
        self._data = data
        self._parent = parent
        self._children = []
    
    def _set_data(self, data):
        self._data = data
    
    def _get_data(self):
        return self._data
    
    def _set_parent(self, new_parent):
        if not isinstance(new_parent, Node):
            raise ValueError("invalid parent type")
        if new_parent == self:
            raise ValueError("invalid parent")
        if new_parent == self.parent:
            return
        if self.parent:
            self.parent.remove(self)

        new_parent.add(self)
        self._parent = new_parent
    
    def _get_parent(self):
        return self._parent
    
    def _set_children(self, children):
        raise Exception("invalid operation")
    
    def _get_children(self):
        return self._children
    
    data = property(_get_data, _set_data)
    parent = property(_get_parent, _set_parent)
    children = property(_get_children, _set_children)
    
    def size(self):
        if not self._children:
            return 1
        else:
            return self.rec_size()
    
    def rec_size(self):
        if not self._children:
            return 1
        s = 1
        for child in self._children:
            s += child.rec_size()
        return s
    
    def add(self, n):
        """Adds the node containing data to this node.

        Params:
            n: the node to add, can be an existing Node.
        """
        if not isinstance(n, Node):
            n = Node(n, self)
        self._children.append(n)
        return n
    
    def remove(self, n):
        """Tries to remove the given node from this tree.

        Params:
            n: the node to remove.
        """
        if not isinstance(n, Node):
            raise ValueError(f"illegal type: {type(n)} is not of type {type(Node)}")
        elif self == n:
            raise ValueError(f"node cannot remove itself")
        self.rec_remove(n)
    
    def rec_remove(self, n):
        if self._children:
            if n in self._children:
                self._children.remove(n)
            else:
                for child in self._children:
                    child.rec_remove(n)
    
    def for_each_top(self, callback, *args, **kwargs):
        """Run callback for each node in the tree top to bottom.
        """
        if self._children:
            callback(self, *args, **kwargs)
            for child in self._children:
                child.for_each_top(callback, *args, **kwargs)
        else:
            callback(self, *args, **kwargs)
    
    def for_each_bottom(self, callback, *args, **kwargs):
        """Run callback for each node in the tree bottom up.
        """
        if self._children:
            for child in self._children:
                child.for_each_bottom(callback, *args, **kwargs)
            callback(self, *args, **kwargs)
        else:
            callback(self, *args, **kwargs)
    
    @staticmethod
    def build_tree(dictionary):
        """Builds a new tree given a dictionary conforming to json.
        """
        nodes = []
        if isinstance(dictionary, dict):
            for k, v in dictionary.items():
                root_node = Node(k)
                root_node.rec_build_tree(v)
                nodes.append(root_node)
        else:
            raise ValueError("invalid data: no tree structure")
        
        if len(nodes) == 1:
            return nodes[0]
        else:
            return nodes

    def rec_build_tree(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                node = self.add(k)
                node.rec_build_tree(v)
        elif isinstance(d, list):
            for v in d:
                self.rec_build_tree(v)
        elif isinstance(d, str):
            self.add(d)