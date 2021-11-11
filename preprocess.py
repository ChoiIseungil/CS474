# Written by Seungil Lee, Nov 11, 2021

import json
import re
import glob
import nltk

stopwords = nltk.corpus.stopwords.words('english')

def preprocess(text):
    text = text.lower()
    text = text.encode('ascii','ignore')
    text = text.decode()                            #remove non ascii characters 
    text = re.sub("[\[\(\{].*?[\]\)\}]", "", text)  #괄호 안 제거
    text = re.sub(r'[^a-zA-Z\u00c0-\u00FF0-9\s]', '', text)
    return text


def main():
    files = []
    for file in glob.glob("./raw_data/*.json"): files.append(file)


    with open('./data.txt','w') as f:
        for file in files:
            j = open(file,'r')
            data = json.load(j)
            titles = data["title"]
            bodies = data["body"]
            for key in titles:
                f.write(titles[key] + ' ' + bodies[key] + '\n')

    f.close()

if __name__ == "__main__":
    main()