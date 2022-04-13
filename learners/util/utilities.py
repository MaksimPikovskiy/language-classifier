import time
import sys

from learners.data_structs.Example import Example


def usage(train_flag, predict_flag):
    print("Error: Incorrect number of arguments", file=sys.stderr)
    time.sleep(0.1)
    if train_flag:
        print("To train the classifier algorithm: ")
        print("\tjava lab3.java train <examples> <hypothesisOut> <learningType>")
    if predict_flag:
        print("To predict with the classifier algorithm: ")
        print("\tjava lab3.java predict <hypothesisFile> <dataFile>")
    sys.exit()


def parse(file, test_flag):
    lines = []

    for line in open(file, encoding="UTF-8"):
        lines.append(Example(line, test_flag))

    return lines
