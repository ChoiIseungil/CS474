import os
from keybert import KeyBERT

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


implicit()

file_path = "/home/cs474/CS474/data.txt"

preprocessed_file = open(file_path, 'r')
file_read = preprocessed_file.read()
preprocessed_file.close()
spl = file_read.split('\n')

'''
text = ""
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
        ""
'''

text = spl[0]

print(text, '\n')

kw_model = KeyBERT()
keywords = kw_model.extract_keywords(text, keyphrase_ngram_range = (1, 5), stop_words=None)

# pip install googletrans==4.0.0-rc1
from googletrans import Translator
'''
translator = Translator()
for k, p in keywords:
    keywords_ko = translator.translate(k,           dest='ko', src='en').text
    keywords_en = translator.translate(keywords_ko, dest='en', src='ko').text
    print(f'{p}: {k} -> {keywords_ko} -> {keywords_en}')
'''

translator = Translator(service_urls = ["papago.naver.com"])
for k, p in keywords:
    keywords_ko = translator.translate(k,           dest='ko', src='en').text
    keywords_en = translator.translate(keywords_ko, dest='en', src='ko').text
    print(f'{p}: {k} -> {keywords_ko} -> {keywords_en}')