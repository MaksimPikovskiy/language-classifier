import pickle
import sys
import os.path

from learners.util.utilities import usage
from learners.DecisionTree import DecisionTree
from learners.AdaBoost import AdaBoost

PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = PATH + "\\input\\"
OUTPUT_PATH = PATH + "\\output\\"


def main():
    if len(sys.argv) < 2:
        usage(True, True)

    action_type = sys.argv[1]

    if action_type == "train":
        if len(sys.argv) <= 4:
            usage(True, False)

        examples_file = sys.argv[2]
        output_file = sys.argv[3]
        learning_type = sys.argv[4]

        if not os.path.isfile(INPUT_PATH + examples_file):
            print("Error: File for Examples was not found!", file=sys.stderr)
            sys.exit()

        model = None
        if learning_type == "dt":
            print("Training Decision Tree Model...")
            model = DecisionTree(INPUT_PATH + examples_file, OUTPUT_PATH + output_file, 7)
        elif learning_type == "ada":
            print("Training AdaBoost Model...")
            model = AdaBoost(INPUT_PATH + examples_file, OUTPUT_PATH + output_file, 5)
        else:
            print("Error: Unknown learning type for Wikipedia Language Classifier Algorithm", file=sys.stderr)
            sys.exit()
        print("Training is complete!")
        model.train()

    elif action_type == "predict":
        if len(sys.argv) <= 3:
            usage(False, True)

        hypothesis_file = sys.argv[2]
        data_file = sys.argv[3]

        if not os.path.isfile(OUTPUT_PATH + hypothesis_file):
            print("Error: No Hypothesis File was found!", file=sys.stderr)
            usage(True, False)
        elif not os.path.isfile(INPUT_PATH + data_file):
            print("Error: No Data File was found to test!", file=sys.stderr)
            sys.exit()

        h_file = open(OUTPUT_PATH + hypothesis_file, "rb")
        model = pickle.load(h_file)

        h_file.close()
        model.predict(INPUT_PATH + data_file)

    else:
        print("Error: Unknown action for Wikipedia Language Classifier Algorithm", file=sys.stderr)
        sys.exit()


if __name__ == '__main__':
    main()
