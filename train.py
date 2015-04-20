"""
Trains a classifier for identifying bots in user agents.

Usage:
    train.py [-c N [-s SCORE]] -o <MODEL> <DATABASE>

Options:
    -o <MODEL>      Filename of the output trained model.
    -c N            N-Cross fold validation. No model is written. [default: 10]
    -s SCORE        Report on SCORE when doing cross-fold validation. [default: f1]
    -h,--help       Shows usage instructions.
"""

import logging
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import scipy.sparse as sp
from docopt import docopt

import util
from features import extract_features


logger = logging.getLogger()

args = docopt(__doc__)

def train(samples, vocabulary):
    logger.debug("Extracting features")
    
    X = []
    for s in samples:
        X.append(extract_features(s[0], vocabulary))
    X = sp.vstack(X, format='csr')

    y = np.array([s[1] for s in samples])

    clf = RandomForestClassifier(n_estimators=30)
    
    if int(args["-c"]):
        logger.debug("Performing N-fold cross-validation (N=%s)" % args["-c"])
        scores = cross_validation.cross_val_score(clf, X.toarray(), y,
                                                    cv=int(args["-c"]),
                                                    scoring=args["-s"])
        print("F1: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
    
    logger.debug("Training model on all data")
    clf.fit(X.toarray(), y)
    
    logger.debug("Done, returning model and vocabulary")
    
    return (clf, vocabulary)


if __name__ == "__main__":
    # Write pickled classifier to stdout.

    import cPickle as pickle
    import sys

    logging.basicConfig(level=logging.DEBUG)
    
    samples, vocabulary = util.read(args["<DATABASE>"])
    
    pickle.dump(train(samples, vocabulary), open(args["-o"], "wb"))
