import pickle
import sys
import os.path

from learners.util.utilities import usage
from learners.DecisionTree import DecisionTree
from learners.AdaBoost import AdaBoost

PATH = os.path.dirname(os.path.abspath(__file__))   # absolute path to this file
INPUT_PATH = PATH + "\\input\\"                     # absolute path to input folder
OUTPUT_PATH = PATH + "\\output\\"                   # absolute path to output folder

# Set these for desired depth/ensemble_size
# ~~~~~~~~~~~~~~~~~~~~~
DEPTH = 7
ENSEMBLE_SIZE = 5
# ~~~~~~~~~~~~~~~~~~~~~

def main():
    """
    Starts the application by reading the given arguments.

    :return: none
    """
    # check if there is train/predict argument
    if len(sys.argv) < 2:
        print("Error: Incorrect number of arguments", file=sys.stderr)
        usage(True, True)

    action_type = sys.argv[1]   # train/predict argument

    if action_type == "train":
        # check if all required arguments for training are provided
        if len(sys.argv) <= 4:
            print("Error: Incorrect number of arguments", file=sys.stderr)
            usage(True, False)

        examples_file = sys.argv[2]
        output_file = sys.argv[3]
        learning_type = sys.argv[4]

        # check if the example file exists
        if not os.path.isfile(INPUT_PATH + examples_file):
            print("Error: File for Examples was not found!", file=sys.stderr)
            sys.exit()

        model = None
        if learning_type == "dt":
            print("Training Decision Tree Model...")
            model = DecisionTree(INPUT_PATH + examples_file, OUTPUT_PATH + output_file, DEPTH)
        elif learning_type == "ada":
            print("Training AdaBoost Model...")
            model = AdaBoost(INPUT_PATH + examples_file, OUTPUT_PATH + output_file, ENSEMBLE_SIZE)
        else:
            print("Error: Unknown learning type for Wikipedia Language Classifier Algorithm", file=sys.stderr)
            sys.exit()
        print("Training is complete!")
        model.train()

    elif action_type == "predict":
        # check if all required arguments for predicting are provided
        if len(sys.argv) <= 3:
            print("Error: Incorrect number of arguments", file=sys.stderr)
            usage(False, True)

        hypothesis_file = sys.argv[2]
        data_file = sys.argv[3]

        # check if hypothesis file exists and check if test file exists
        if not os.path.isfile(OUTPUT_PATH + hypothesis_file):
            print("Error: No Hypothesis File was found!", file=sys.stderr)
            usage(True, False)
        elif not os.path.isfile(INPUT_PATH + data_file):
            print("Error: No Data File was found to test!", file=sys.stderr)
            sys.exit()

        # load the file and use it to predict
        h_file = open(OUTPUT_PATH + hypothesis_file, "rb")
        model = pickle.load(h_file)
        h_file.close()
        model.predict(INPUT_PATH + data_file)

    else:
        print("Error: Unknown action for Wikipedia Language Classifier Algorithm", file=sys.stderr)
        sys.exit()


if __name__ == '__main__':
    main()
