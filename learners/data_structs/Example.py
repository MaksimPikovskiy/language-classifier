class Example:
    classification = None
    words = None
    features = None
    weight = None

    def __init__(self, example, test_example_flag):
        if test_example_flag:
            self.classification = None
            self.words = example
        else:
            self.classification = example[:2]
            self.words = example[2:]
        self.features = self.get_features(example)

    def get_features(example):
        pass