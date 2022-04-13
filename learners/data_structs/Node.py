class Node:
    """
    A class used to represent a node in the Decision Tree.

    Attributes
    ------------
    is_leaf : boolean
        flag to show whether the node is leaf or not
    value : str
        the classification of the Node
    children : dictionary of Nodes
        the children Nodes that are divided based on classification
    weight : int
        the weight of the Node, which is used for AdaBoost

    Methods
    ------------
    add_child(label, node)
        adds a child Node to this Node under the branch label.
    decide(example)
        decides the language of the example

    """
    is_leaf = False
    value = None
    children = None
    weight = None

    def __init__(self, value, is_leaf):
        """
        Initializes Node of Decision Tree.

        :param value: the classification of the Node.
        :param is_leaf: flag whether this Node is leaf or not.
        """
        self.is_leaf = is_leaf
        self.value = value
        self.children = {}
        self.weight = None

    def add_child(self, label, node):
        """
        Adds a child to this Node under branch label.

        :param label: the label for the branch
        :param node: the child node
        :return: none
        """
        self.children[label] = node

    def decide(self, example):
        """
        Decides the language classification of the example.

        :param example: the example to get the classification for.
        :return: classification of the example.
        """
        node = self

        while node:
            if node.is_leaf:
                return node.value

            branch = example.attributes[node.value]

            if branch in node.children:
                node = node.children[branch]
            else:
                return get_majority(node)

        return None


def get_majority(node):
    """
    Get the majority classification for the node.

    :param node: the node to get the majority classification for.
    :return: majority classification
    """
    if node.is_leaf:
        return node.value

    if not node.children:
        return None

    count = {}
    max_count = -1
    max_classification = None

    for child in node.children:
        classification = get_majority(node.children[child])
        if not classification:
            continue

        if classification in count:
            count[classification] += 1
        else:
            count[classification] = 1

        if count[classification] > max_count:
            max_count = count[classification]
            max_classification = classification

    return max_classification
