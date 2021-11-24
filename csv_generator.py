# Written by Seungil Lee, Nov 25, 2021

import json
import re
import glob
import nltk
import contractions
import csv

nltk.download('stopwords')
STOPWORDS = set(nltk.corpus.stopwords.words('english'))
STOPWORDS.remove('s')

def preprocess(text):
    text = re.sub("[\[\(\{].*?[\]\)\}]", " ", text)                                     # 1. remove words in the parentheses
    text = re.sub("\S*@\S*\s?|(http[s]?S+)|(w+.[A-Za-z]{2,4}S*)", " ", text)            # 2. remove email address and ur.s
    text = text.lower()                                                                 # 3. lower
    text = re.sub("u.s."," usa ",text)                                                  # 4. corner case u.s. (appeared 15052 times..!)
    text = text.replace("'s", " ")                                                      # 5. remove apostrophes with s (it appears a lot)
    text = text.replace(".",". ")                                                       # 6. sentence seperate problem
    text = text.encode('ascii','ignore').decode()                                       # 7. remove non ascii characters
    text = contractions.fix(text)                                                       # 8. expand contractions
    text = re.sub("[^\w. -]|_", " ", text)                                              # 9. erase except -, ., alphanumerics
    text= " ".join([word for word in str(text).split() if word not in STOPWORDS])       # 10. remove stopwords
    text = re.sub("north korea|n. korea","nkorea",text)                                # 11. corner case n.korea 
    text = re.sub("south korea|s. korea","skorea",text)                                # 12. corner case s.korea
    return text


def main():
    files = []
    for file in glob.glob("./raw_data/*.json"): files.append(file)

    with open('./data/data.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(["title","body","time","section"])
        for file in files:
            print(file, " in progress")
            j = open(file,'r')
            data = json.load(j)
            titles = data["title"]
            bodies = data["body"]
            dates = data["time"]
            sections = data["section"]
            for key in titles:
                title = titles[key]
                body = preprocess(title) + ' ' + preprocess(bodies[key])
                date = dates[key].split()[0]
                section = sections[key]
                writer.writerow([title,body,date,section])
            j.close()

    f.close()

    print("Finished")


if __name__ == "__main__":
    main()