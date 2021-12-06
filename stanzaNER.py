# Written by Seungil Lee, Nov 21 2021
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
# https://medium.com/@b.terryjack/nlp-pretrained-named-entity-recognition-7caa5cd28d7b

import stanza
import csv

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

def ner(document):
    doc = nlp(document)
    result = dict()
    for sent in doc.sentences:
        for ent in sent.ents:
            if ent.type in result:
                result[ent.type].add(ent.text)
            else:
                result[ent.type] = set()
                result[ent.type].add(ent.text)
    return result

def main():
    raw = open('./data/2017.tsv','r')
    new = open('./data/2017_ner.tsv','w')
    
    reader = csv.reader(raw,delimiter = '\t')
    headers = next(reader,None)
    writer = csv.writer(new,delimiter = '\t')
    if headers:
        writer.writerow(headers)
    for row in reader:
        row[9] = ner(row[1])
        writer.writerow(row)

    raw.close()
    new.close()

if __name__ == '__main__':
    main()
