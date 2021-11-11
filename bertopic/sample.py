import os
from bertopic import BERTopic
topic_model = BERTopic()
file_path = "/home/cs474/CS474/data.txt"
of = open(file_path, 'r')
rf = of.read()
of.close()
splitted = rf.split('\n')
topics, probs = topic_model.fit_transform(splitted)
print(topic_model.get_topic_info())
print(topic_model.get_topic(0))