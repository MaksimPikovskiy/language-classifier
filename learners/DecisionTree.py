import pickle

from util.utilities import parse
from data_structs.Node import Node


class DecisionTree:
    train_data = []
    test_data = []
    output_file = None
    decision_tree = None

    def __init__(self, examples_file, output_file):
        lines = parse(examples_file, False)

        self.train_data = lines
        self.output_file = output_file

    def train(self):

        self.decision_tree = self.create_tree(self.train_data, )

        file = open(self.output_file, "wb")
        pickle.dump(self, file)
        file.close()

    def predict(self, test_file):
        self.test_data = parse(test_file, True)

        for example in self.test_data:
            decision = self.decision_tree.decide(example)
            print("Result: ", decision, "| Line: ", example.words)


def create_tree(examples, attributes, parent_examples):
    if not examples:
        return plurality_value(parent_examples)
    elif same_classification(examples):
        return Node(examples[0].classification, True)
    if not attributes:
        return Node(plurality_value(examples), True)
    else:
        attribute = max_importance(examples, attributes)
        root = Node(attribute, False)


def plurality_value(examples):
    majority_classification = None
    max_weight = -1
    count = {}

    for example in examples:
        weight = example.weight if example.weight else 1
        if example.classification in count:
            count[example.classification] += weight
        else:
            count[example.classification] = weight

    for example in examples:
        if count[example.classification] > max_weight:
            max_weight = count[example.classification]
            majority_classification = example.classification

    return majority_classification


def same_classification(examples):
    classification = examples[0].classification

    for example in examples:
        if example.classification != classification:
            return False

    return True


