import math
import pickle

from .util.utilities import parse
from .data_structs.Node import Node


class DecisionTree:
    """
    A class used to represent a training/prediction model which uses Decision Tree.

    Attributes
    ------------
    train_data : array of Examples
        an array of Examples, which have a classification, features, and 15 words (and weight)
    test_data : array of Examples
        an array of Examples, which have features and 15 words (and weight)
    output_file : str
        file location to where to save the trained logic (best tree)
    decision_tree : Node
        root of the entire Decision Tree
    depth : int
        maximum depth for the Decision Tree

    Methods
    ------------
    train()
        trains the Decision Tree based on provided Examples
    predict(test_file)
        predicts the language of the line given in provided
        test file based on trained Decision Tree
    """
    train_data = []
    test_data = []
    output_file = None
    decision_tree = None
    depth = 0

    def __init__(self, examples_file, output_file, depth):
        """
        Initializes Decision Tree Training/Prediction Model.

        :param examples_file: file containing lines with classification.
        :param output_file: file location to where to save the Decision Tree.
        :param depth: maximum depth for the Decision Tree.
        """
        lines = parse(examples_file, False)

        self.train_data = lines
        self.output_file = output_file
        self.depth = depth

    def train(self):
        """
        Creates a Decision Tree with provided training data and data's attributes with given depth.

        :return: none
        """
        self.decision_tree = create_tree(self.train_data, set(self.train_data[0].attributes.keys()), [], self.depth)

        file = open(self.output_file, "wb")
        pickle.dump(self, file)
        file.close()

    def predict(self, test_file):
        """
        Reads in the data in test file and lets the Decision Tree decide whether the Example is in English or Dutch.
        Prints the classification of each Example(line) into terminal.

        :param test_file: the test file containing the data with 15 words and their attributes.
        :return: none
        """
        self.test_data = parse(test_file, True)

        for example in self.test_data:
            decision = self.decision_tree.decide(example)
            print("Result:", decision, "| Line:", example.words.replace("\n", ""))


def create_tree(examples, attributes, parent_examples, depth):
    """
    Creates a Decision Tree for the examples and their attributes, with specified depth.

    :param examples: the examples to create the Decision Tree for.
    :param attributes: the attributes of examples.
    :param parent_examples: the original examples (all examples).
    :param depth: maximum depth for the decision Tree.
    :return: the root of the Decision Tree (aka entire created Decision Tree).
    """
    if not examples:
        return plurality_value(parent_examples)
    elif same_classification(examples):
        return Node(examples[0].classification, True)
    if not attributes:
        return Node(plurality_value(examples), True)
    else:
        attribute, children = max_importance(examples, attributes)
        root = Node(attribute, False)

        # if an illegal depth was given or calculated, set it to one
        if depth < 1:
            depth = 1

        for child in children:
            subtree = None
            temp_examples = children[child]

            # if depth is 1, create a leaf node, else continue creating subtrees
            if depth == 1:
                subtree = Node(plurality_value(temp_examples), is_leaf=True)
            else:
                subtree = create_tree(temp_examples, attributes.difference({attribute}), examples, depth - 1)
            root.add_child(child, subtree)

        return root


def count_examples_per_classification(examples):
    """
    Count the number of examples for each classification that examples have.

    :param examples: the examples.
    :return: dictionary which counts the counts for each classification.
    """
    count = {}

    for example in examples:
        weight = example.weight if example.weight else 1
        if example.classification in count:
            count[example.classification] += weight
        else:
            count[example.classification] = weight

    return count


def calculate_entropy(examples):
    """
    Calculate the entropy for the given examples.

    :param examples: the examples.
    :return: calculated entropy of the provided examples.
    """
    count = count_examples_per_classification(examples)
    entropy = 0

    for classification in count.keys():
        p = count[classification]/len(examples)
        entropy += -p * math.log(p, 2)

    return entropy


def plurality_value(examples):
    """
    Get the classification that is the majority of provided examples.

    :param examples: the examples.
    :return: the majority classification.
    """
    majority_classification = None
    max_weight = -1
    count_for_classifications = count_examples_per_classification(examples)

    for example in examples:
        if count_for_classifications[example.classification] > max_weight:
            max_weight = count_for_classifications[example.classification]
            majority_classification = example.classification

    return majority_classification


def same_classification(examples):
    """
    Check if all provided examples have same classification.

    :param examples: the examples.
    :return: true if all of them have same classification.
             false, otherwise.
    """
    classification = examples[0].classification

    for example in examples:
        if example.classification != classification:
            return False

    return True


def gain_for_attribute(examples, attribute):
    """
    Calculate the information gain for the provided attribute.

    :param examples: the provided examples.
    :param attribute: the provided attribute.
    :return: information gain for the attribute, and
             the children of the attribute that are split based on the classification.
    """
    entropy = calculate_entropy(examples)
    count = len(examples)
    children = split_on_attribute(examples, attribute)
    total = 0

    for child in children:
        children_of_child = children[child]
        total += (len(children_of_child)/count) * calculate_entropy(children_of_child)

    info_gain = entropy - total

    return info_gain, children


def max_importance(examples, attributes):
    """
    Retrieves the attribute with the highest information gain and its children.

    :param examples: the provided examples
    :param attributes: the attributes of the provided examples
    :return: the attribute with the highest information gain and the split children
    """
    max_gain = -1
    max_attribute = None
    children = None

    for attribute in attributes:
        gain, split_children = gain_for_attribute(examples, attribute)
        if gain > max_gain:
            max_gain = gain
            max_attribute = attribute
            children = split_children

    return max_attribute, children


def split_on_attribute(examples, attribute):
    """
    Splits the provided examples based on the attribute.

    :param examples: the provided examples.
    :param attribute: the attribute to split the examples on.
    :return: dictionary containing the examples split based on attribute and classification.
    """
    split = {}

    for example in examples:
        classification = example.attributes[attribute]
        if classification in split:
            split[classification].append(example)
        else:
            split[classification] = [example]

    return split
