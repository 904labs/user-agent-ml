import re
import cPickle as pickle
from features import extract_features

class user_agent_ml:
    def __init__(self, model):
        """ Requires the filename of the model to open """
        self.clf, self.vocabulary = pickle.load(open(model, "rb"))
    
    def predict(self, ua):
        """Predict if a patient is diagnosed with a disease."""
        
        if re.search(r"urllib|nagios|spider|bot|google|http_request|jeeves|yahoo|http", ua, re.IGNORECASE) is not None:
            return True

        X = extract_features(ua, self.vocabulary)
        pred = self.clf.predict(X.toarray())
        if not pred[0]:
            return True

        return False
