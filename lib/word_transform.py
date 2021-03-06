from absl import app, flags
from functools import partial
import string  

flags.DEFINE_spaceseplist("features", None, "Features taken into account")
flags.DEFINE_string("input", None, "Input path")
flags.DEFINE_string("output", None, "Output path")
flags.DEFINE_string("vocabulary", None, "vocabulary")
flags.DEFINE_string("bases", None, "vocabulary")
flags.DEFINE_string("supertags", None, "vocabulary")
flags.DEFINE_string("suffixes", None, "vocabulary")
flags.DEFINE_string("prefixes", None, "vocabulary")

vocab = set()
superbases = {}
supertags = {}
suffixes = set()
prefixes = set()

def _load_set(path, data_set):
    with open(path, "r") as ifile:
        for line in ifile:
            line = line if line[-1] != "\n" else line[:-1]
            data_set.add(line)

def _load_dict(path, data_dict):
    with open(path, "r") as ifile:
        for line in ifile:
            line = line if line[-1] != "\n" else line[:-1]
            splitted_line = line.split(" ")
            data_dict[splitted_line[0]] = splitted_line[-1]

def load_vocabulary(path):
    global vocab
    _load_set(path, vocab)

def load_prefixes(path):
    global prefixes
    _load_set(path, prefixes)

def load_suffixes(path):
    global suffixes
    _load_set(path, suffixes)

def load_supertags(path):
    global supertags
    _load_dict(path, supertags)

def load_superbases(path):
    global superbases
    _load_dict(path, superbases)

def get_prefix(word, k):
    return f"iPj{word[:k]}"

def get_suffix(word, k):
    return f"iSj{word[-k:]}"

def get_word(word):
    return "iWj"+word

def get_suffix_word(word):
    word_lower = word.lower()
    if word_lower in vocab:
        return "iWj"+word
    n = len(word)
    for k in range(n):
        if word_lower[k:] in suffixes:
            return "iSj"+word[k:]
    return "iSj"

def get_prefix_word(word):
    word_lower = word.lower()
    if word_lower in vocab:
        return "iWj"+word
    n = len(word)
    for k in range(n):
        if word_lower[:-k] in prefixes:
            return "iPj"+word[:-k]
    return "iPj"

def get_prefix_suffix_word(word):
    prefix = get_prefix_word(word)
    if prefix[:3] == "iWj":
        return prefix
    return prefix + get_suffix_word(word)

def get_supertag(word, k = 5):
    word_lower = word.lower()
    if word_lower in vocab:
        return "iWj"+word
    if word_lower in supertags:
        return "iTj"+supertags[word_lower]
    return get_suffix(word, k)

def get_basis(word):
    word_lower = word.lower()
    if word_lower in superbases:
        return "iBj"+superbases[word_lower]
    return "iWj"+word

def get_method(identifier):
    if identifier == "W":
        return get_word
    if identifier == "T":
        return get_supertag
    if identifier == "B":
        return get_basis
    if identifier == "PSW":
        return get_prefix_suffix_word
    if identifier == "PW":
        return get_prefix_word
    if identifier == "SW":
        return get_suffix_word
    if identifier[0] == "S":
        return partial(get_suffix, k = int(identifier[1:]))
    if identifier[0] == "P":
        return partial(get_prefix, k = int(identifier[1:]))

FLAGS = flags.FLAGS

def apply_methods(word, methods):
    if word in string.punctuation:
        return word
    res = [m(word) for m in methods]
    return " ".join(res)