import pickle
import math

from .util.utilities import parse
from .DecisionTree import create_tree
from .data_structs.WeightedInstance import WeightedInstance


class AdaBoost:
    """
    A class used to represent a training/prediction model which uses AdaBoost.

    Attributes
    ------------
    train_data : array of Examples
        an array of Examples, which have a classification, features, 15 words, and weight
    test_data : array of Examples
        an array of Examples, which have features, 15 words, and weight
    output_file : str
        file location to where to save the trained logic (best ensemble)
    ensemble : array of Decision Trees (Stumps)
        an array of Decision Trees (stumps)
    ensemble_size : int
        maximum size of ensemble for the AdaBoost

    Methods
    ------------
    train()
        trains the AdaBoost based on provided Examples
    predict(test_file)
        predicts the language of the line given in provided
        test file based on trained AdaBoost
    weighted-majority(example)
        classifies the Example by collecting the decisions
        from the ensemble and returns the classification that
        is a majority
    """
    train_data = []
    test_data = []
    output_file = None
    ensemble = []
    ensemble_size = 7

    def __init__(self, examples_file, output_file, ensemble_size):
        """
        Initializes AdaBoost Training/Prediction Model.

        :param examples_file: file containing lines with classification.
        :param output_file: file location to where to save the AdaBoost.
        :param ensemble_size: maximum size of ensemble for the AdaBoost.
        """
        lines = parse(examples_file, False)

        self.train_data = lines
        self.output_file = output_file
        self.ensemble_size = ensemble_size

    def train(self):
        """
        Creates an AdaBoost ensemble with provided training data and data's attributes with given ensemble size.

        :return: none
        """
        self.ensemble = []
        attributes = set(self.train_data[0].attributes.keys())
        n = len(self.train_data)
        # e = 1 / (2 * n)   # logic from pseudocode
        instance = WeightedInstance(self.train_data)

        for i in range(self.ensemble_size):
            stump = create_tree(self.train_data, attributes, [], 1)
            error = 0.0

            for example in self.train_data:
                decision = stump.decide(example)

                # calculate the error for incorrectly classified
                if decision != example.classification:
                    error += example.weight

            # this logic (from pseudocode) messes the AdaBoost, resulting in None classification
            # if error > 0.5:
            #     break
            # error = min(error, 1 - e)
            error = 0.0000000000001 if error == 0 else error

            # go through every example and update weights
            for j in range(n):
                example = self.train_data[j]
                decision = stump.decide(example)

                # if the example was correctly classified, lower the weight of the example
                if decision == example.classification:
                    # new_weight = example.weight * (error/(1 - error))
                    new_weight = example.weight * (error / (instance.initial_sum - error))
                    instance.change_weight(j, new_weight)

            instance.normalize()            # normalize the sum of the Weighted Instance
            # stump.weight = (1/2) * (math.log(1 - error)/error)
            stump.weight = (1/2) * (math.log(instance.initial_sum - error) / error)    # math.log is natural log (ln)
            self.ensemble.append(stump)     # add the stump to ensemble

        file = open(self.output_file, "wb")
        pickle.dump(self, file)
        file.close()

    def predict(self, test_file):
        """
        Reads in the data in test file and lets the AdaBoost ensemble decide whether the Example is in English or Dutch.
        Prints the classification of each Example(line) into terminal.

        :param test_file: the test file containing the data with 15 words and their attributes.
        :return: none
        """
        self.test_data = parse(test_file, True)

        for example in self.test_data:
            decision = self.weighted_majority(example)
            print(decision)
            # print("Result:", decision, "| Line:", example.words.replace("\n", ""))

    def weighted_majority(self, example):
        """
        Classifies the Example by collecting the decisions from the ensemble and returns the classification that
        is a majority.

        :param example: the example to get classification for
        :return: majority classification for the Example
        """
        count = {}
        max_count = 0
        majority = None

        for stump in self.ensemble:
            decision = stump.decide(example)

            if decision in count:
                count[decision] += stump.weight
            else:
                count[decision] = stump.weight

            if count[decision] > max_count:
                max_count = count[decision]
                majority = decision

        return majority
