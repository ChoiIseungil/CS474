import os
from keybert import KeyBERT

file_path = "/home/cs474/CS474/data.txt"

preprocessed_file = open(file_path, 'r')
file_read = preprocessed_file.read()
preprocessed_file.close()
spl = file_read.split('\n')

text = """
            Supervised learning is the machine learning task of learning a function that
            maps an input to an output based on example input-output pairs. It infers a
            function from labeled training data consisting of a set of training examples.
            In supervised learning, each example is a pair consisting of an input object
            (typically a vector) and a desired output value (also called the supervisory signal). 
            A supervised learning algorithm analyzes the training data and produces an inferred function, 
            which can be used for mapping new examples. An optimal scenario will allow for the 
            algorithm to correctly determine the class labels for unseen instances. This requires 
            the learning algorithm to generalize from the training data to unseen situations in a 
            'reasonable' way (see inductive bias).
        """

text = spl[0]

# print(text)

kw_model = KeyBERT()
keywords = kw_model.extract_keywords(text, keyphrase_ngram_range = (1, 5), stop_words=None)

for k, p in keywords:
    print(p, k)
