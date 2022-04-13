import time
import sys

from learners.data_structs.Example import Example


def usage(train_flag, predict_flag):
    """
    Prints usage messages for train and predict statements.

    :param train_flag: flag to display "train" usage message.
    :param predict_flag: flag to display "predict" usage message.
    :return: none
    """
    time.sleep(0.1)  # used to make sure these usage messages are printed after the error
    if train_flag:
        print("To train the classifier algorithm: ")
        print("\tjava lab3.java train <examples> <hypothesisOut> <learningType>")
    if predict_flag:
        print("To predict with the classifier algorithm: ")
        print("\tjava lab3.java predict <hypothesisFile> <dataFile>")
    sys.exit()


def parse(file, test_flag):
    """
    Converts the lines of data file into Example data structure.

    :param file: the file to read and convert lines into Examples.
    :param test_flag: flag to tell if the file contains training data or testing data.
    :return: an array of Examples.
    """
    examples = []

    for line in open(file, encoding="UTF-8"):
        examples.append(Example(line, test_flag))

    return examples
