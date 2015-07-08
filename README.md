# Detect bots from user agent strings
User-agent-ml detects whether a user agent string refers to a bot or 
to a legitimate browser. The method is hybrid: it is based on rules and machine
learning. The rule based part allows for high efficiency since most bot hits
come from well known sources (e.g., search engines), and the machine learning 
part allows detection of less well known user agent strings or new ones, which 
it would have been hard to capture with a solely rule based system. 

## Usage
```python
import user_agent_ml
uaml = user_agent_ml.user_agent_ml("../data/user-agent.model")
uaml.predict("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12")
>>> False
uaml.predict("Mozilla/5.0 (compatible; DotBot/1.1; http://www.opensiteexplorer.org/dotbot, help@moz.com)")
>>> True
```
The `.predict("user-agent-string")` function returns `True` if the user agent
string is identified as bot, and `False` if it is identified as a regular
browser. 

## Performance
System effectiveness, measured in weighted
[F1-score](https://en.wikipedia.org/wiki/F1_score), is at 99.11% (± 0.0303).
Reported performance is the average over 10-fold cross validation on 53,829
records taking into account class imbalance; 50,918 examples of (mobile)
browsers and 2,911 examples of bots).

## Machine learning
User-agent-ml at its core uses a decision tree classifier (Random Forest).
Features are mostly of textual nature, e.g., a vocabulary was created from all
tokens in the user agent strings. More elaborate features, and elaborate
feature selection methods are likely to further increase classification
effectiveness–however, this is left for future versions.

###### Acknowledgements
User-agent-ml is developed by [904Labs B.V.](http://904labs.com) User-agent-ml
uses training data from project [MAUL](https://github.com/bholley/maul). The
code skeleton for machine learning was taken from project
[NERD](https://github.com/larsmans/nerd). The development of user-agent-ml was
partially supported by [Europeana](http://europeana.eu), the European Cultural
Heritage Search Engine.
