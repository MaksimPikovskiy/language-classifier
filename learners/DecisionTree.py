import pickle


class DecisionTree:
    train_data = []
    test_data = []
    output_file = None
    decision_tree = None

    def __init__(self, examples_file, output_file):


