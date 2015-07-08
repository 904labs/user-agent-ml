"""
Tests the classifier on a given file.

Usage:
    predict.py <MODEL> <DATABASE>

Options:
    -h,--help       Shows usage instructions.
"""
from features import extract_features
from docopt import docopt

import util

args = docopt(__doc__)

def predict(clf, ua, vocabulary):
    """Predict if a patient is diagnosed with a disease."""

    X = extract_features(ua, vocabulary)
    pred = clf.predict(X.toarray())

    return X, pred


if __name__ == "__main__":
    import cPickle as pickle
    import sys

    clf, vocabulary = pickle.load(open(args["<MODEL>"], "rb"))

    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s clf input_file" % sys.argv[0]
        sys.exit(1)

    count = 0
    correct = 0
    samples, _ = util.read(args["<DATABASE>"])
    for ua, label in samples:
        X, Y_pred = predict(clf, ua, vocabulary)
        count += 1
        if label == Y_pred:
            correct += 1
        else:
            print ua, label, Y_pred[0]
            print X
            print
            
        
    print "Total: %d, Correct: %d, Ratio: %.2f" % (count, correct, (1.*correct/count))
