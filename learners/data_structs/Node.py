class Node:
    is_leaf = False
    value = None
    children = None
    weight = None

    def __init__(self, value, is_leaf):
        self.is_leaf = is_leaf
        self.value = value
        self.children = {}
        self.weight = None