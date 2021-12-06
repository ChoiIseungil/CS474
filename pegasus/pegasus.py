import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import numpy as np
import os
import csv
from tqdm import tqdm



def find_root():
    cur_path = os.getcwd()
    while(cur_path[-5:] != "CS474"): 
        cur_path = os.path.dirname(cur_path)
    return cur_path+"/"

def get_response(input_text, model):
    batch = tokenizer([input_text],truncation=True,padding='longest',max_length=1024, return_tensors="pt").to(torch_device)
    gen_out = model.generate(**batch,max_length=128,num_beams=5, num_return_sequences=1, temperature=1.5)
    output_text = tokenizer.batch_decode(gen_out, skip_special_tokens=True)
    return output_text

def generate_summary_event(model, temp_true = False):
    data_dir = find_root()+"data/"
    temp_dir = find_root()+"bertopic/temp_data/"
    file_type = ".tsv"
    end = "_event"
    for year in range(2015,2018):
        print(year)
        if temp_true:
            file = temp_dir + str(year) + file_type
        else:
            file = data_dir + str(year) + file_type
        of = open(file, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        up_dt = []
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

        # event
        if temp_true:
            file = temp_dir + str(year) + end + file_type
        else:
            file = data_dir + str(year) + end + file_type
        of = open(file, 'r')
        dt_event = csv.DictReader(of, delimiter='\t')
        up_dt =[]
        issue_idx = []
        event_idx = []
        rep_idx = []
        key_ = []     
        temp = tqdm(dt_event)
        for r in temp:
            temp.set_description("reading events for year %s" % str(year))
            issue_idx.append(r['issue'])
            event_idx.append(r['event'])
            rep_idx.append(r['representativedoc'])
            key_.append(r['keyword'])
        of.close()

        temp =tqdm(range(len(issue_idx)))
        for i in temp:
            temp.set_description("saving event summary information for year %s" % str(year))
            row = { 'issue': issue_idx[i],
                    'event': event_idx[i],
                    'representativedoc': rep_idx[i],
                    'keyword': key_[i],
                    'summary': get_response(raw_docs[int(rep_idx[i])], model)
                    }
            up_dt.append(row)

        of = open(file, 'w', newline="")
        headers = ["issue","event","representativedoc","keyword", "summary"]
        data = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(up_dt)
        of.close()


    return


def generate_summary_issue(model, temp_true = False):
    data_dir = find_root()+"data/"
    temp_dir = find_root()+"bertopic/temp_data/"
    file_type = ".tsv"
    end = "_issue"
    for year in range(2015,2018):
        print(year)
        if temp_true:
            file = temp_dir + str(year) + file_type
        else:
            file = data_dir + str(year) + file_type
        of = open(file, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        up_dt = []
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

        # issue
        if temp_true:
            file = temp_dir + str(year) + end + file_type
        else:
            file = data_dir + str(year) + end + file_type
        of = open(file, 'r')
        dt_event = csv.DictReader(of, delimiter='\t')
        up_dt =[]
        rep_doc_idx = []
        key_ = []
        rel1_ = []
        rel2_ = []
        rel3_ = []
        rel4_ = []
        rel5_ = []
        temp = tqdm(dt_event)
        for r in temp:
            temp.set_description("reading issues for year %s" % str(year))
            rep_doc_idx.append(r['representativedoc'])
            key_.append(r['keyword'])
            rel1_.append(r['related1'])
            rel2_.append(r['related2'])
            rel3_.append(r['related3'])
            rel4_.append(r['related4'])
            rel5_.append(r['related5'])
        of.close()

        temp =tqdm(range(len(rep_doc_idx)))
        for i in temp:
            temp.set_description("saving issue summary information for year %s" % str(year))
            row = { 'representativedoc': rep_doc_idx[i],
                    'keyword': key_[i],
                    'related1': rel1_[i],
                    'related2': rel2_[i],
                    'related3': rel3_[i],
                    'related4': rel4_[i],
                    'related5': rel5_[i],
                    'summary': get_response(raw_docs[int(rep_doc_idx[i])], model)
                    }
            up_dt.append(row)

        of = open(file, 'w', newline="")
        headers = ["representativedoc","keyword","related1","related2","related3","related4","related5", "summary"]
        data = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
        data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(up_dt)
        of.close()


    return




if __name__ == '__main__':
    model_name = 'tuner007/pegasus_summarizer'
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
    #generate_summary_event( model, temp_true = False)
    generate_summary_issue( model, temp_true = False)