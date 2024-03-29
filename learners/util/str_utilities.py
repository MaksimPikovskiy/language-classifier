def ends_in(suffix, words):
    """
    Checks if there is any word in the example that ends with the given suffix

    :param suffix: the suffix
    :param words: words which are part of one Example
    :return: True if there is some word that ends with the suffix.
             False, otherwise
    """
    for word in words:
        if word.endswith(suffix):
            return True

    return False


def pair_range(pair_count):
    """
    Generalizes the attribute. That is, finds a range for
    the pairs that they fall into.

    :param pair_count: a count of pairs
    :return: the range that the pair count falls into
    """
    range_pair = (0, 4)                # first generalized range: 0 => 4
    if 5 <= pair_count <= 8:
        range_pair = (5, 8)            # second generalized range: 5 => 8
    elif 9 <= pair_count <= 11:
        range_pair = (9, 11)           # third generalized range: 9 => 11
    elif 11 < pair_count:
        range_pair = (12, None)        # fourth generalized range: 12 => infinite
    return range_pair
