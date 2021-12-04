# Written by Yoonho Lee, Nov 28, 2021
# Last update: HyeAnn Lee, Dec 02, 2021

from bertopic import BERTopic
import os
import csv
from tqdm import tqdm

def find_root():
    cur_path = os.getcwd()
    while(cur_path[-5:] != "CS474"): 
        cur_path = os.path.dirname(cur_path)
    return cur_path+"/"


def compute_related_topic(temp_true = False):
    data_dir = find_root()+"data/"
    temp_dir = find_root()+"hyeann/"
    file_type = ".tsv"
    end = "_issue"

#    model_iter = iter(topic_models)
    for year in range(2015, 2018):
        print(year)

        ## Load model.
        if temp_true:
            file = temp_dir + "model_" + str(year)
        else:
            file = data_dir + "model_" + str(year)
        model = BERTopic.load(file)
#        model = next(model_iter)

        if temp_true:
            file = temp_dir + str(year) + '_keywordfromtitle' + file_type
        else:
            file = data_dir + str(year) + '_keywordfromtitle' + file_type
    
        up_dt = []
        related_event = [[(0, -1)] * 5 for _ in range(10)]


        # Read 201*.tsv
        of = open(file, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        idx = 0
        for r in dt:
            row = { 'title': r['title'],
                    'rawbody': r['rawbody'],
                    'body': r['body'],
                    'date': r['date'],
                    'keyword': r['keyword'],
                    'issue': r['issue'],
                    'event': r['event'],
                    'relatedissue': None,
                    'similarity': None,
                    'ner': r['ner']}

            relissue_sim = (-1, 0)

            if not int(row['issue']) in range(0, 10):
                # Find most-related issue among top 10, per event.

                keyword, _, _ = row['keyword'].partition(',')

                '''
                title_words = row['title'].split()
                spl = min(5, len(title_words))
                keyword = ' '.join(title_words[:spl])
                '''

                topics, similarity = model.find_topics(keyword)
                for i in range(len(topics)):
                    topic = topics[i]
                    sim = similarity[i]
                    relissue_sim = (topic, sim)
                    if not topic in range(0, 10):
                        continue
                    if sim > related_event[topic][-1][0]:
                        related_event[topic][-1] = (sim, idx)
                        related_event[topic].sort(reverse=True)
                        print(topic, sim, idx)
                    break

            row['relatedissue'], row['similarity'] = relissue_sim
            up_dt.append(row)

            idx = idx + 1
#            if idx%100==0:
#                print("\tline", idx, "...")
        of.close()
        # Close 201*.tsv


        # Write RELATEDISSUE and SIMILARITY on 201*.tsv
        headers = ["title","rawbody","body","date","keyword","issue","event","relatedissue","similarity","ner"]
        of = open(file, 'w', newline="")
        tsv_writer = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        tsv_writer.writerow(dict((heads, heads) for heads in headers))
        tsv_writer.writerows(up_dt)
        of.close()
        # Close 201*.tsv


        # Read 201*_issue.tsv
        if temp_true:
            file = temp_dir + str(year) + end + file_type
        else:
            file = data_dir + str(year) + end + file_type
        up_dt = []
        of = open(file, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        tup_iter = iter(related_event)
        for r in dt:
            info = next(tup_iter)
            row = {'representativedoc': r['representativedoc'],
                    'keyword': r['keyword'],
                    'related1': info[0][1],
                    'related2': info[1][1],
                    'related3': info[2][1],
                    'related4': info[3][1],
                    'related5': info[4][1]}
            up_dt.append(row)
        of.close()
        # Close 201*_issue.tsv


        # Write RELATED* on 201*_issue.tsv
        headers = ["representativedoc","keyword","related1","related2","related3","related4","related5"]
        if temp_true:
            file = temp_dir + str(year) + '_keywordfromtitle' + end + file_type
        else:
            file = data_dir + str(year) + '_keywordfromtitle' + end + file_type
        of = open(file, 'w', newline="")
        tsv_writer = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        tsv_writer.writerow(dict((heads, heads) for heads in headers))
        tsv_writer.writerows(up_dt)
        of.close()
        # Close 201*_issue.tsv

    return


if __name__ == '__main__':
    compute_related_topic(temp_true = True)
