# Written by Seungil Lee, Nov 25, 2021

import json
import re
import glob
import nltk
import contractions
import csv

YEAR = "2017"
nltk.download('stopwords')
STOPWORDS = set(nltk.corpus.stopwords.words('english'))
STOPWORDS.remove('s')

def preprocess(text):
    text = text.encode('ascii','ignore').decode()                                       # 9. remove non ascii characters
    text = re.sub("[\[\(\{].*?[\]\)\}]", " ", text)                                     # 1. remove words in the parentheses
    text = re.sub("\S*@\S*\s?|(http[s]?S+)|(w+.[A-Za-z]{2,4}S*)", " ", text)            # 2. remove email address and ur.s
    text = text.lower()                                                                 # 3. lower
    text = re.sub("u.s."," usa ",text)                                                  # 4. corner case u.s. (appeared 15052 times..!)
    text = re.sub("north korea|n. korea|n. k.","nkorea",text)                           # 5. corner case n.korea 
    text = re.sub("south korea|s. korea|s. k.","skorea",text)                           # 6. corner case s.korea
    text = text.replace("'s", " ")                                                      # 7. remove apostrophes with s (it appears a lot)
    text = text.replace(".",". ")                                                       # 8. sentence seperate problem
    text = contractions.fix(text)                                                       # 10. expand contractions
    text = re.sub("[^\w. -]|_", " ", text)                                              # 11. erase except -, ., alphanumerics
    text= " ".join([word for word in str(text).split() if word not in STOPWORDS])       # 12. remove stopwords
    return text


def main():
    files = []
    for file in glob.glob("./raw_data/*.json"): files.append(file)

    with open('./data/' + YEAR + '.tsv','w') as f:
        writer = csv.writer(f,delimiter = '\t')
        writer.writerow(["title","rawbody","body","date","keyword","issue","event","relatedissue","similarity","ner"])
        for file in files:
            print(file, " in progress")
            j = open(file,'r')
            data = json.load(j)
            titles = data["title"]
            bodies = data["body"]
            dates = data["time"]
            for key in titles:
                title = titles[key]
                raw_body = bodies[key].replace('\n',' ')
                body = preprocess(title) + ' ' + preprocess(raw_body)
                year, month, day = tuple((dates[key].split()[0]).split('-'))
                if year == YEAR:  writer.writerow([title,raw_body,body,month+'-'+day,None,None,None,None,None,None])
                else: continue
            j.close()

    f.close()

    print("Finished")


if __name__ == "__main__":
    main()