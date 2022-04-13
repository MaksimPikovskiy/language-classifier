class WeightedInstance:
    """
    A class used to represent a Weighted Instance (or sample) for AdaBoost.

    Attributes
    ------------
    data : array of Examples
        Examples for this Weighted Instance
    sum : int
        the weight of this Weighted Instance
    initial_sum : float
        the normalized weight of this Weighted Instance

    Methods
    ------------
    normalize()
        normalizes the sum/weight of this Weighted Instance
    change_weight(i, new_weight)
        changes the weight of data at index i and adjusts the sum to that change
    """
    data = None
    sum = 0
    initial_sum = 0

    def __init__(self, examples):
        """
        Initializes Weighted Instance.

        :param examples: the examples to be contained in this Weighted Instance.
        """
        self.data = examples

        for example in self.data:
            example.weight = 1
            self.sum += example.weight

        self.initial_sum = self.sum

    def normalize(self):
        """
        Normalizes the weight of this Weighted Instance.

        :return: none
        """
        normalization_constant = self.initial_sum / self.sum
        self.sum = 0
        for example in self.data:
            example.weight *= normalization_constant
            self.sum += example.weight

    def change_weight(self, i, new_weight):
        """
        Changes the weight of the data at index i and adjusts the sum to that change.

        :param i: the index of the data in the Weighted Instance to change the weight for.
        :param new_weight: the new weight for the data at index i
        :return: none
        """
        self.sum -= self.data[i].weight
        self.data[i].weight = new_weight
        self.sum += new_weight
