import collections
import itertools
import string
from nltk import ngrams, sent_tokenize, word_tokenize

def get_top_count_of_phrases_from_passage(passage, *args, **kwargs):
    """

    :param passage:
    :param args:
    :param kwargs:
    :return:
    >>> passage = "The quick brown fox jumped over the lazy dog. \
    The lazy dog, peeved to be labeled lazy, jumped over a snoring turtle. \
    In retaliation the quick brown fox jumped over ten snoring turtles. \
    Then the quick brown fox refueled with some ice cream."
    >>> grams = get_top_count_of_phrases_from_passage(passage)
    >>> grams
    ['the lazy dog', 'the quick brown fox jumped over']

    """
    #TODO: pass in kwargs for begin/end
    n_grams = get_grams_for_passage(passage, strip_punctuation=True, lowercase=True)

    #TODO: pass in min_count as kwarg
    phrase_list = [" ".join(phrase) for phrase in n_grams]
    min_count_dict = make_count_dict_of_repeat_phrases(phrase_list)

    #remove subphrases
    sieved_min_count_dict = sieve_dict_for_sub_phrases(min_count_dict)

    #TODO: get top K count from kwargs
    return sieved_min_count_dict.most_common(10)

def get_range_of_grams(tokens, n_min, n_max):
    """
    Get a list of n-gram tuples representing a list of tokens

    :param tokens: a list of strings
    :param n_min: min-length of n-grams
    :param n_max: max length of n-grams
    :return: a list of n-grams represented as tuples of strings
    >>> tokens = ['apple', 'Apple', 'bob']
    >>> get_range_of_grams(tokens, 2, 3)
    [('apple', 'Apple'), ('Apple', 'bob'), ('apple', 'Apple', 'bob')]
    """
    grams = []
    for i in range(n_min, (n_max+1)):
        #TODO pass in grams? Conditionally exclude append if it is a subphrase?
        grams.extend(list(ngrams(tokens, i)))

    return grams

def split_passage_into_sentences(passage):
    '''
    Given a passage, will return a list of strings within the passage, where each string represents a sentence

    :param passage: a string with potentially multiple sentences
    :return:  a list of un-cleaned strings representing sentences
    '''
    return sent_tokenize(passage)

def get_grams_for_passage(passage,
                          n_min=3,
                          n_max=10,
                          strip_punctuation=False,
                          lowercase=False,
                          *args, **kwargs):
    """
    return a list of n-grams for a passage, where sentence boundaries are respected

    :param passage: input string containing one or more sentences
    :param begin_n: min token count of a phrase
    :param end_n: max token count of a phrase
    :param strip_puntuation: if False, then punctuation will stay. Else will be stripped
    :param lowercase: if False, then case will be respected. Else lowercase will be forced for return grams
    :return: a list of all n_min -> n_max grams in passage, delineated by sentence

    >>> passage = "apple apple apple Apple. bob. cat, cat."
    >>> grams = get_grams_for_passage(passage, n_min=2, n_max=3, strip_punctuation=True, lowercase=True)
    >>> grams
    [('apple', 'apple'), ('apple', 'apple'), ('apple', 'apple'), ('apple', 'apple', 'apple'), ('apple', 'apple', 'apple'), ('cat', 'cat')]


    """

    #convert to sentences using nltk
    sentences = sent_tokenize(passage)
    n_grams = []
    for sentence in sentences:
        word_tokens = word_tokenize(sentence)
        if strip_punctuation:
            word_tokens = [word for word in word_tokens if word not in string.punctuation]
        if lowercase:
            word_tokens = [word.lower() for word in word_tokens]
        n_grams.extend(get_range_of_grams(word_tokens, n_min, n_max))

    return n_grams

def make_count_dict_of_repeat_phrases(phrase_list, min_count=2):
    '''
    :param phrase_list: a list of string phrases
    :param min_count: the minimum count allowed within the returned list

    :return: a dict of {Phrase: Count} where only a count > min_count is present

    >>> x = ["a", "a", "b", "c", "d", "D"]
    >>> ret_val = make_count_dict_of_repeat_phrases(x)
    >>> ret_val
    Counter({'a': 2})
    '''
    count_dict = collections.Counter(phrase_list)

    #dropwhile only checks while the test holds true. most_common is a Counter Iterable
    # that returns a descending sorted list of keys
    #read like: drop everything that is >= min_count from out delete list, then delete all keys that didn't make cut
    for key, count in itertools.dropwhile(lambda key_count: key_count[1] >= min_count, count_dict.most_common()):
        del count_dict[key]

    return count_dict

def sieve_dict_for_sub_phrases(dictionary):
    """
    sieve a dictionary for keys that are substrings of other keys

    :param dictionary: Some Dictionary or Counter to sieve
    :return: a new Counter with only the keys that passed the sieve

    >>> x = {"car": 0, "magic carpet":1, "the car port":2, "cargo plane":3, "the car port at house": 4}
    >>> y = sieve_dict_for_sub_phrases(x)
    >>> y
    Counter({'the car port at house': 4, 'cargo plane': 3, 'magic carpet': 1})
    """

    #get keys
    strings = dictionary.keys()
    sieved_set = set(dictionary.keys())
    #sort by length
    strings = sorted(strings, key=len)
    #for each phrase, check if its a substring of a larger phrase
    for i in range(len(strings)-1): #no need to check last string
        check_string = strings[i]
        if is_phrase_a_substring_in_list(check_string, strings[i+1:]):
            sieved_set.discard(check_string)

    return collections.Counter({key:dictionary[key] for key in sieved_set})

def is_phrase_a_substring_in_list(phrase, check_list):
    """

    :param phrase: string to check if Substring
    :param check_list: list of strings to check against
    :return: True if phrase is a substring of any in check_list, otherwise false

    >>> x = ["apples", "bananas", "coconuts"]
    >>> is_phrase_a_substring_in_list("app", x)
    True

    >>> is_phrase_a_substring_in_list("blue", x)
    False
    """
    return any(phrase in x for x in check_list)


if __name__ == "__main__":
    import doctest
    doctest.testmod()