# Written by Seungil Lee, Nov 11, 2021

import json
import re
import glob
import nltk
import contractions

nltk.download('stopwords')
STOPWORDS = set(nltk.corpus.stopwords.words('english'))


def preprocess(text):
    text = re.sub("[\[\(\{].*?[\]\)\}]", "", text)                                      # 1. remove words in the parentheses
    text = text.encode('ascii','ignore').decode()                                       # 2. remove non ascii characters
    text = re.sub("b[w-.]+?@w+?.w{2,4}b", "", text)                                     # 3. remove email address
    text = re.sub("(http[s]?S+)|(w+.[A-Za-z]{2,4}S*)", "", text)                        # 4. remove urls
    text = text.lower()                                                                 # 5. lower
    text = contractions.fix(text)                                                       # 6. expand contractions
    text= " ".join([word for word in str(text).split() if word not in STOPWORDS])       # 7. remove stopwords
    return text


def main():
    files = []
    for file in glob.glob("./raw_data/*.json"): files.append(file)

    print("Started")

    with open('./data.txt','w') as f:
        for file in files:
            j = open(file,'r')
            data = json.load(j)
            titles = preprocess(data["title"])
            bodies = preprocess(data["body"])
            for key in titles:
                f.write(titles[key] + ' ' + bodies[key] + '\n')

    f.close()

    print("Finished")


if __name__ == "__main__":
    main()