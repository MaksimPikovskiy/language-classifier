# lab3: Language Classifier

## Usage
Place your desired training and testing data files into `lab3/input` folder. After training
the Classifier, it will generate object file with the given output file name in `lab3/output`
directory.

* `train <examples> <hypothesisOut> <learning-type>` to read the labeled examples and perform training ("ada" or "dt").
  * `examples` is a file containing labeled examples.
  * `hypothesisOut` specifies the file name to write your model to.
  * `learning-type` specifies the type of learning algorithm you want to run, it is either "dt" or "ada". 
    * *You can edit the desired `DEPTH` and `ENSEMBLE_SIZE` in `lab3.py` file.*
* `predict <hypothesis> <file>` to classify each line as either English or Dutch using the specified hypothesis.
  * `hypothesis` is a trained decision tree or ensemble created by the classifier
    * *It will be in `lab3/output` directory. Simply put the name of the file and it will read it from directory*
  * `file` is a file containing lines of 15 word sentence fragments in either English or Dutch.

### Example Usage
> *Remember to place the testing and training data files into `lab3/input` directory.*

Train an AdaBoost model:
* `train main_train.dat ensemble.oj ada`

Let AdaBoost model predict the classifications of sentences in test data file:
* `predict ensemble.oj main_test.dat`

Train a Decision Tree model:
* `train main_train.dat tree.oj dt`

Let Decision Tree model predict the classifications of sentences in test data file:
* `predict tree.oj main_test.dat`