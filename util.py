import sqlite3
import collections
import re

def read(dbfilename):
    # Open Database
    conn = sqlite3.connect(dbfilename)
    conn.text_factory = str
    c = conn.cursor()

    # Query
    c.execute('SELECT uaString, Type FROM data')
    
    counter = 0
    vocabulary = {}
    samples = []
    for item in c:
        if item[1] in ["Browser", "Mobile Browser"]:
            label = 1
        else:
            label = 0
        uaString = item[0]
        samples.append((uaString, label))
        for token in gentokenlist(uaString):
            if token not in vocabulary:
                vocabulary[token] = counter
                counter += 1
    return samples, vocabulary


def gentokenlist(uaString):
    tokenlist = []
    for x in re.split('[.(),;/\s]',uaString):
        x = x.strip().rstrip()
        if not x == "":
            # number check            
            x = rewrite(x)
            tokenlist.append(x)

    return tokenlist

def rewrite(x): # Performs various token rewrites

    # Strip whitespace
    x = x.strip().rstrip()

    # Rewrite numbers to their length
    if x.isdigit():
        return str(len(x)) # return length of number

    # Rewrite the common +http: token to http:
    elif x == "+http:":
      return "http:"

    # Common case - return the original string
    else:
        return x
