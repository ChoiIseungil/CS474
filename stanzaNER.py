# Written by Seungil Lee, Nov 21 2021
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
# https://medium.com/@b.terryjack/nlp-pretrained-named-entity-recognition-7caa5cd28d7b

import stanza

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

def ner(document):
    doc = nlp(document)
    result = set()
    for sent in doc.sentences:
        for ent in sent.ents:
            result.add((ent.text, ent.type))
    return result

def main():
    raw = open('./raw_data.txt','r')
    new = open('./stanza_ner.txt','w')


    for line in raw: 
        new.write(str(ner(line))+'\n')

    raw.close()
    new.close()

if __name__ == '__main__':
    main()
