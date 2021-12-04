# Written by Yoonho Lee, Nov 28, 2021
# Last update: HyeAnn Lee, Dec 02, 2021

import numpy as np
from bertopic import BERTopic
import os
import csv
from tqdm import tqdm

def find_root():
    cur_path = os.getcwd()
    while(cur_path[-5:] != "CS474"): 
        cur_path = os.path.dirname(cur_path)
    return cur_path+"/"

def extract_topic(temp_true = False):
    data_dir = find_root()+"data/"
    temp_dir = find_root()+"hyeann/"
    file_type = ".tsv"
    end = "_issue"

#    models = []
    for year in range(2015, 2018):
        if temp_true:
            file = temp_dir + str(year) + file_type
        else:
            file = data_dir + str(year) + file_type
        
        titles = []
        raw_docs = []
        docs = []
        dates = []
        keywords = []
        issues = []
        events = []
        related_issues = []
        related_similarities = []
        ners = []


        # Read 201*.tsv
        of = open(file, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        temp = tqdm(dt)
        for r in temp:
            temp.set_description("reading data for year %s" % str(year))
            titles.append(r['title'])
            raw_docs.append(r['rawbody'])
            docs.append(r['body'])
            dates.append(r['date'])
            keywords.append(r['keyword'])
            issues.append(r['issue'])
            events.append(r['event'])
            related_issues.append(r['relatedissue'])
            related_similarities.append(r['similarity'])
            ners.append(r['ner'])
        of.close()
        # Close 201*.tsv


        ## Topic Modeling
        topic_model = BERTopic(min_topic_size=20, top_n_words=8)
        topics, _ = topic_model.fit_transform(docs)
        issues = topics


        # Write ISSUE on 201*.tsv
        up_dt = []
        temp = tqdm(range(len(titles)))
        for i in temp:
            temp.set_description("saving issues of documents for year %s" % str(year))
            row = { 'title': titles[i],
                    'rawbody': raw_docs[i],
                    'body': docs[i],
                    'date': dates[i],
                    'keyword': keywords[i],
                    'issue': issues[i],
                    'event': events[i],
                    'relatedissue': related_issues[i],
                    'similarity': related_similarities[i],
                    'ner': ners[i]}
            up_dt.append(row)
        
        of = open(file, 'w', newline="")
        headers = ["title","rawbody","body","date","keyword","issue","event","relatedissue","similarity","ner"]
        data = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(up_dt)
        of.close()
        # Close 201*.tsv


        ## issue

        ## Get representative document per issue
        R_doc = topic_model.get_representative_docs()
        up_dt =[]
        temp = tqdm(range(10))
        for i in temp:
            temp.set_description("Saving representative document information for year %s" % str(year))
            doc_id = docs.index(R_doc[i][0])
            row = { 'representativedoc': doc_id,
                    'keyword': None,
                    'related1': None,
                    'related2': None,
                    'related3': None,
                    'related4': None,
                    'related5': None}
            up_dt.append(row)


        # Create 201*_issue.tsv with REPRESENTATIVEDOC filled.
        if temp_true:
            file = temp_dir + str(year) + end + file_type
        else:
            file = data_dir + str(year) + end + file_type
        of = open(file, 'w', newline="")
        headers = ["representativedoc","keyword","related1","related2","related3","related4","related5"]
        data = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(up_dt)
        of.close()
        # Close 201*_issue.tsv


        ## Save model.
        if temp_true:
            file = temp_dir + "model_" + str(year)
        else:
            file = data_dir + "model_" + str(year)
        topic_model.save(file)
#        models.append(topic_model)

    return
#    return models


def extract_event(temp_true = False):
    data_dir = find_root()+"data/"
    temp_dir = find_root()+"hyeann/"
    file_type = ".tsv"
    end = "_event"


    for year in range(2015, 2018):
        if temp_true:
            file = temp_dir + str(year) + file_type
        else:
            file = data_dir + str(year) + file_type
        
        
        issue_event_pair = []
        titles = []
        raw_docs = []
        docs = []
        dates = []
        keywords = []
        issues = []
        events = []
        related_issues = []
        related_similarities = []
        ners = []


        # Read 201*.tsv
        of = open(file, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        temp = tqdm(dt)
        for r in temp:
            temp.set_description("reading data for year %s" % str(year))
            titles.append(r['title'])
            raw_docs.append(r['rawbody'])
            docs.append(r['body'])
            dates.append(r['date'])
            keywords.append(r['keyword'])
            issues.append(r['issue'])
            events.append(r['event'])
            related_issues.append(r['relatedissue'])
            related_similarities.append(r['similarity'])
            ners.append(r['ner'])
        of.close()
        # Close 201*.tsv


        ## Topic Modeling
        topic_docs = {topic: [] for topic in set(issues)}
        for topic, doc in zip(issues, docs):
            topic_docs[topic].append(doc)        
        temp = tqdm(range(-1,len(topic_docs)-1))
        for topic_iter in temp:
            temp.set_description("extracting events for year %s" % str(year))
            topic_model = BERTopic(min_topic_size=3, top_n_words=8, nr_topics=5)
            docs_of_topic = topic_docs[str(topic_iter)]
            event_cluster, _ = topic_model.fit_transform(docs_of_topic)
            for event_iter in range(len(docs_of_topic)):
                events[docs.index(docs_of_topic[event_iter])] = event_cluster[event_iter]
            if topic_iter>=0 and topic_iter<10:
                R_doc = topic_model.get_representative_docs()
                for R_iter in range(min(5,len(R_doc))):
                    issue_event_pair.append([topic_iter, R_iter, docs.index(R_doc[R_iter][0])])


        # Write EVENT on 201*.tsv
        up_dt = []
        temp = tqdm(range(len(titles)))
        for i in temp:
            temp.set_description("saving events of documents for year %s" % str(year))
            row = { 'title': titles[i],
                    'rawbody': raw_docs[i],
                    'body': docs[i],
                    'date': dates[i],
                    'keyword': keywords[i],
                    'issue': issues[i],
                    'event': events[i],
                    'relatedissue': related_issues[i],
                    'similarity': related_similarities[i],
                    'ner': ners[i]}
            up_dt.append(row)
        
        of = open(file, 'w', newline="")
        headers = ["title","rawbody","body","date","keyword","issue","event","relatedissue","similarity","ner"]
        data = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(up_dt)
        of.close()
        # Close 201*.tsv



        ## event
        
        up_dt =[]
        temp =tqdm(range(len(issue_event_pair)))        
        for i in temp:
            temp.set_description("Saving representative event information for year %s" % str(year))
            row = { 'issue': issue_event_pair[i][0],
                    'event': issue_event_pair[i][1],
                    'representativedoc': issue_event_pair[i][2],
                    'keyword': None}
            up_dt.append(row)


        # Create 201*_event.tsv with REPRESENTATIVEDOC filled.
        if temp_true:
            file = temp_dir + str(year) + end + file_type
        else:
            file = data_dir + str(year) + end + file_type
        of = open(file, 'w', newline="")
        headers = ["issue","event","representativedoc","keyword"]
        data = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(up_dt)
        of.close()
        # Close 201*_event.tsv

    return


def compute_related_topic(topic_models, temp_true = False):
    data_dir = find_root()+"data/"
    temp_dir = find_root()+"hyeann/"
    file_type = ".tsv"
    end = "_issue"

    model_iter = iter(topic_models)
    for year in range(2015, 2018):
        model = next(model_iter)
        if temp_true:
            file = temp_dir + str(year) + file_type
        else:
            file = data_dir + str(year) + file_type
    
        up_dt = []
        related_event = [[(0, -1)] * 5 for _ in range(10)]
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
            
            if not int(row['issue']) in range(0, 10):
                keyword, _, _ = row['keyword'].partition(',')
                topics, similarity = model.find_topics(keyword)
                for i in range(len(topics)):
                    topic = topics[i]
                    sim = similarity[i]
                    if not topic in range(0, 10):
                        continue
                    row['relatedissue'] = topic
                    row['similarity'] = sim
                    if sim > related_event[topic][-1][0]:
                        related_event[topic][-1] = (sim, idx)
                        related_event[topic].sort(reverse=True)
                    break
            up_dt.append(row)

            idx = idx + 1
            if idx%100==0:
                print("\tline", idx, "...")
        of.close()


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

        headers = ["representativedoc","keyword","related1","related2","related3","related4","related5"]
        of = open(file, 'w', newline="")
        tsv_writer = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        tsv_writer.writerow(dict((heads, heads) for heads in headers))
        tsv_writer.writerows(up_dt)
        of.close()

    return


if __name__ == '__main__':
    topic_models = extract_topic(temp_true = True)
    extract_event(temp_true = True)
#    extract_topic()
#    extract_event()
#    compute_related_topic(topic_models, temp_true = True)
