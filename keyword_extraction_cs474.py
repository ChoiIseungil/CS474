# 03 Dec 2021, HyeAnn Lee

import six
from google.cloud import translate_v2 as translate
import csv
from keybert import KeyBERT
from tqdm import tqdm

kw_model = KeyBERT()
translate_client = translate.Client()
years = ['2015', '2016', '2017']

def translate_text(target, text):

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]



def keybert_entire_doc():

    for year in years:
        print(year, " tsv ......")

        file_path = "./hyeann/" + year + ".tsv"
        up_dt = []

        # Read 201*.tsv
        of = open(file_path, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        temp = tqdm(dt)
#        count = 0
        for r in temp:
            temp.set_description("Extracting & Translating keyword for year %s" % str(year))
#            count = count + 1
            row = { 'title': r['title'],
                    'rawbody': r['rawbody'],
                    'body': r['body'],
                    'date': r['date'],
                    'keyword': None,
                    'issue': r['issue'],
                    'event': r['event'],
                    'relatedissue': r['relatedissue'],
                    'similarity': r['similarity'],
                    'ner': r['ner']}
            
            text = row['rawbody']
            keywords = kw_model.extract_keywords(text, keyphrase_ngram_range = (1, 4), stop_words=None)
            
            up_kw = ''
            for keyword, _ in keywords:
                kor = translate_text('ko', keyword)
                keyword = translate_text('en', kor)
                up_kw = up_kw + keyword + ','
            row['keyword'] = up_kw[:-1]

            up_dt.append(row)

#            if count%20==0:
#                print("\tline", count, "...")

        of.close()
        # Close 201*.tsv

        # Write KEYWORD on 201*.tsv
        file_path = "./hyeann/" + year + "_keywordtranslated.tsv"
        of = open(file_path, 'w', newline="")
        headers = ["title","rawbody","body","date","keyword","issue","event","relatedissue","similarity","ner"]
        tsv_writer = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        tsv_writer.writerow(dict((heads, heads) for heads in headers))
        tsv_writer.writerows(up_dt)
        of.close()
        # Close 201*.tsv

        print(year, "tsv completed")



if __name__ == '__main__':
    keybert_entire_doc()
