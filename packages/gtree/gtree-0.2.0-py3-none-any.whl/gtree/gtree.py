
class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
    
    def size(self):
        if not self.children:
            return 1
        else:
            return self.rec_size()
    
    def rec_size(self):
        if not self.children:
            return 1
        s = 1
        for child in self.children:
            s += child.rec_size()
        return s
    
    def add(self, n):
        """Adds the node containing data to this node.

        Params:
            n: the node to add, can be an existing Node.
        """
        if not isinstance(n, Node):
            n = Node(n, self)
        self.children.append(n)
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
        if self.children:
            if n in self.children:
                self.children.remove(n)
            else:
                for child in self.children:
                    child.rec_remove(n)
    
    def for_each_top(self, callback, *args, **kwargs):
        """Run callback for each node in the tree top to bottom.
        """
        if self.children:
            callback(self, *args, **kwargs)
            for child in self.children:
                child.for_each_top(callback, *args, **kwargs)
        else:
            callback(self, *args, **kwargs)
    
    def for_each_bottom(self, callback, *args, **kwargs):
        """Run callback for each node in the tree bottom up.
        """
        if self.children:
            for child in self.children:
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