import sys
import os.path

from learners.util.utilities import usage
from learners.DecisionTree import DecisionTree
from learners.AdaBoost import AdaBoost

PATH = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2:
        usage(True, True)

    type = sys.argv[1]

    if type == "train":
        if len(sys.argv) <= 4:
            usage(True, False)

        examples_file = sys.argv[2]
        output_file = sys.argv[3]
        learning_type = sys.argv[4]

        if not os.path.isfile(PATH + examples_file):
            print("Error: File for Examples was not found!", file=sys.stderr)
            sys.exit()

        model = None
        if learning_type == "ada":
            pass
            model = DecisionTree(examples_file, output_file)
        elif learning_type == "dt":
            pass
            model = AdaBoost(examples_file, output_file)
        else:
            print("Error: Unknown learning type for Wikipedia Language Classifier Algorithm", file=sys.stderr)
            sys.exit()
        model.train()

    elif type == "predict":
        if len(sys.argv) <= 3:
            usage(False, True)

        hypothesis_file = sys.argv[2]
        data_file = sys.argv[3]

        if not os.path.isfile(hypothesis_file):
            print("Error: No Hypothesis File was found!", file=sys.stderr)
            usage(True, False)
        elif not os.path.isfile(data_file):
            print("Error: No Data File was found to test!", file=sys.stderr)
            sys.exit()

    else:
        print("Error: Unknown action for Wikipedia Language Classifier Algorithm", file=sys.stderr)
        sys.exit()


if __name__ == '__main__':
    main()