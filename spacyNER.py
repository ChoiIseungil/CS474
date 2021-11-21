# Written by Seungil Lee, Nov 21 2021
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
# https://medium.com/@b.terryjack/nlp-pretrained-named-entity-recognition-7caa5cd28d7b

import spacy
sp_lg = spacy.load('en_core_web_lg')

def ner(document):
    return str({(ent.text.strip(), ent.label_) for ent in sp_lg(document).ents})

raw = open('./raw_data.txt','r')
new = open('./spacy_ner.txt','w')


for line in raw: 
    new.write(ner(line)+'\n')

raw.close()
new.close()
