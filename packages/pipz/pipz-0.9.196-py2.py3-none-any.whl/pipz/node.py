class node(object):
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []

    def append_child(self, node):
        node.parent = self
        self.children.append(node)

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'