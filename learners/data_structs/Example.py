from learners.util.str_utilities import ends_in, pair_range


class Example:
    """
    A class used to represent each given example

    Attributes
    ------------
    classification : str
        the language classification of the example
    line : str
        the 15 words of this example
    attributes : dictionary of boolean, range, and int
        the attributes of this example (e.g. presence of English articles, etc.)
    weight : int
        the weight of this example (used in AdaBoost)

    Methods
    ------------
    get_attributes(example)
        scans for attributes of the example
    vow_con_pairs_and_ratio()
        calculates the number of vowel pairs (e.g. "oo"), the number of consonant
        pairs (e.g. "tt") and the vowel:consonant ratio
    avg_word_len()
        finds the average word length and generalizes it into one of three ranges
    """
    classification = None
    line = None
    attributes = None
    weight = None

    def __init__(self, example, test_example_flag):
        """
        Initializes the Example.
        Checks whether it is training example or test example.

        :param example: the example
        :param test_example_flag: flag which shows whether it is a test example or not
        """
        if test_example_flag:
            self.classification = None
            self.line = example.lower()
        else:
            self.classification = example[:2]
            self.line = example[3:]
        self.attributes = self.get_attributes()

    def get_attributes(self):
        """
        Finds all of the declared attributes for the example.

        :return: none
        """
        vow_pairs, con_pairs, vow_con_ratio = self.vow_con_pairs_and_ratio()
        words = set(self.line.split())

        return {
            # Dutch sentences attributes
            "ends-in-en": ends_in("en", words),
            "ends-in-e": ends_in("e", words),
            "has-aa": "aa" in self.line,
            "has-ee": "ee" in self.line,
            "has-word-en": "en" in words,
            "has-article-de": "de" in words,
            "has-article-het": "het" in words,
            "has-article-een": "een" in words,
            "has-article-der": "der" in words,
            "has-article-des": "des" in words,
            "has-article-den": "den" in words,
            # English sentences attributes
            "has-word-she": "she" in words,
            "has-word-he": "he" in words,
            "has-word-they": "they" in words,
            "has-word-it": "it" in words,
            "has-article-the": "the" in words,
            "has-article-a": "a" in words,
            "has-article-an": "an" in words,
            "has-word-and": "and" in words,
            "has-word-or": "or" in words,
            "has-word-in": "in" in words,
            "has-word-of": "of" in words,
            # Other attributes
            "vow_con_ratio": vow_con_ratio,
            "avg_word_len": self.avg_word_len(),
            "vowel-pairs": vow_pairs,
            "consonant-pairs": con_pairs,
            "letter-pairs": pair_range(sum([self.line[i] == self.line[i - 1] for i in range(1, len(self.line))]))
                            # finds a pair range to find letter pairs, like "oo" or "tt"

        }

    def vow_con_pairs_and_ratio(self):
        """
        Calculates the number of vowel pairs (e.g. "oo"),
        the number of consonant pairs (e.g. "tt") and
        the vowel:consonant ratio.

        :return: range for vowel pairs, range for consonant pairs,
                 and vowel:consonant ratio.
        """
        vowels = {"a", "e", "i", "o", "u"}

        vow_count = 0
        con_count = 0
        i = 0
        while i < len(self.line) - 1:
            char = self.line[i]
            next_char = self.line[i + 1]
            # count vowels
            if char in vowels and char == next_char:
                vow_count += 1
                i += 2
            # count consonants
            elif char == next_char:
                con_count += 1
                i += 2
            # go to next character
            else:
                i += 1

        vowel_total = 0
        consonant_total = 0
        for char in self.line:
            if char in vowels:
                vowel_total += 1
            elif 97 <= ord(char) <= 122:    # 97 => 122, lowercase vowels and consonants (no symbols)
                consonant_total += 1
            else:
                continue

        ratio = vowel_total / consonant_total
        ratio_range = (0, 0.5)          # first generalized range: 0 => 0.5
        if 0.51 <= ratio <= 0.70:
            ratio_range = (0.51, 0.70)  # second generalized range: 0.51 => 0.70
        elif 0.71 <= ratio:
            ratio_range = (0.71, None)  # third generalized range: 0.71 => infinite

        return pair_range(vow_count), pair_range(con_count), ratio_range

    def avg_word_len(self):
        """
        Generalizes the attribute. That is, finds a range for
        the average word length that the average fall into.

        :return: range of the average word length that the average fall into.
        """
        words = self.line.split()
        avg = sum(len(word) for word in words) // len(words)

        range = (0, 5)             # first generalized range: 0 => 5
        if 6 <= avg <= 10:
            range = (6, 10)        # second generalized range: 6 => 10
        elif 11 <= avg:
            range = (11, None)     # second generalized range: 11 => infinite
        return range