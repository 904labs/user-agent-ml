import re
import scipy.sparse as sp

from util import gentokenlist

def extract_features(useragent, vocabulary):
    """Do feature extraction on a single sentence.

    We need a sentence, rather than a token, since some features depend
    on the context of tokens.

    Parameters
    ----------
    sentence : list of string

    vocabulary : dict of (string * int)
        Maps terms to indices.
    """
    tokens = gentokenlist(useragent)
    n_tokens = len(tokens)
    n_features = n_feature_functions + len(vocabulary) + 1
    X = sp.lil_matrix((1, n_features), dtype=int)
        
    X[0, 0] = n_tokens
    for token in tokens:
        # Vocabulary feature
        try:
            X[0, n_feature_functions + 1 + vocabulary[token]] = 1
        except KeyError:
            pass
    return X


# Spelling
def first_of_sentence(s, i):
    return i == 0

def all_caps(s, i):
    return s[i][0].isupper()

def initial_cap(s, i):
    return s[i][0][0].isupper()

def has_dash(s, i):
    return '-' in s[i]

def has_num(s, i):
    return re.search(r"[0-9]", s[i]) is not None

# Feature metafunctions
def conj(fs):
    """Conjunction of features fs"""
    def feature(s, i):
        return all(f(s, i) for f in fs)
    return feature

def butnot(f1, f2):
    def feature(s, i):
        return f1(s, i) and not f2(s, i)
    return feature

def nextf(f, offset=1):
    """Next token has feature f"""
    def feature(s, i):
        i += offset
        return i < len(s) and f(s, i)
    return feature

def prevf(f, offset=1):
    """Previous token has feature f"""
    def feature(s, i):
        i -= offset
        return i >= 0 and f(s, i)
    return feature


# FEATURE_FUNCTIONS = [initial_cap, all_caps, first_of_sentence, has_dash,
#                      #has_num,
#                      #butnot(initial_cap, first_of_sentence),
#                      prevf(initial_cap), prevf(all_caps),
#                      isadj, isadv, isart, isconj, isint, ismisc,
#                      isnoun, isnum, isprep, ispunc, ispron, isverb]
FEATURE_FUNCTIONS = []
n_feature_functions = len(FEATURE_FUNCTIONS)


if __name__ == '__main__':
    import conll
    import sys

    for s in conll.read_file(sys.argv[1]):
        for i in xrange(len(s)):
            print ' '.join(s[i]),
            for f in extract_features(s):
                print '%s:%d' % f,
        print
