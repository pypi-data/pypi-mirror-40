
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
    
    def add_new(self, data):
        """Adds a new node containing data to this node.
        """
        node = Node(data, self)
        self.children.append(node)
        return node
    
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
                node = self.add_new(k)
                node.rec_build_tree(v)
        elif isinstance(d, list):
            for v in d:
                self.rec_build_tree(v)
        elif isinstance(d, str):
            self.add_new(d)