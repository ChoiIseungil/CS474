# Written by Yoonho Lee, Nov 28, 2021

import numpy as np
from bertopic import BERTopic
import os

def find_root():
    cur_path = os.getcwd()
    while(cur_path[-5:] != "CS474"): 
        cur_path = os.path.dirname(cur_path)
    return cur_path+"/"

def extract_topic():
    data_dir = find_root()+"data/"
    file_type = ".tsv"
    for i in range(3):
        file = data_dir + str(2015+i) + file_type
        topic_model = BERTopic(min_topic_size=20, top_n_words=8)
        of = open(file, 'r')
        rf = of.read()
        of.close()
        splitted = rf.split('\n')[1:-1]
        for i in range(len(splitted)):
            temp = splitted[i].split('\t')
            if len(temp) != 10:
                print(i)
                print(len(temp))
                print(splitted[i])
                
        
        '''
        splitted = list(zip(*[a.split('\t') for a in splitted]))
        titles = splitted[0]
        raw_docs = splitted[1]
        docs = splitted[2]
        dates = splitted[3]
        keywords = splitted[4]
        issues = splitted[5]
        events = splitted[6]
        related_issues = splitted[7]
        related_similarities = splitted[8]
        ners = splitted[9]
        print(docs[0])
        topics, _ = topic_model.fit_transform(docs)
        issues = topics
        '''
        break
    return 



def extract_event():
    data_dir = find_root()+"data/"
    file_type = ".tsv"
    topic_model = BERTopic(min_topic_size=3, top_n_words=8, nr_topics=5)



    return
'''
topic_model = BERTopic(min_topic_size=20, top_n_words = 8)
file_path = "/home/cs474/CS474/data/data.tsv"

of = open(file_path, 'r')
rf = of.read()
of.close()
splitted = rf.split('\n')[1:-1]
splitted = list(zip(*[[a.split('\t')[0], '\t'.join(a.split('\t')[1:-2]), a.split('\t')[-2], a.split('\t')[-1]] for a in splitted]))

titles = splitted[0]
docs = splitted[1]
dates = splitted[2]
sections = splitted[3]
topics, probs = topic_model.fit_transform(docs)
print(len(topic_model.get_topic_info()))
print(topic_model.get_topic_info()[:30])

# get documents per class
topic_docs = {topic: [] for topic in set(topics)}
for topic, doc in zip(topics, docs):
    topic_docs[topic].append(doc)
'''


if __name__ == '__main__':
    extract_topic()
    extract_event()