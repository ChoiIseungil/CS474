# 02 Dec 2021, HyeAnn Lee

import csv

years = ['2015', '2016', '2017']

def match_keyword(year, rep_docs_id, up_dt, file_path, headers):
    # Read 201*.tsv
    file_path_docs = "./hyeann/" + year + ".tsv"
    of = open(file_path_docs, 'r')
    dt = csv.DictReader(of, delimiter='\t')
    line_num = 0
    for r in dt:
        if line_num in rep_docs_id:
            idx = rep_docs_id.index(line_num)
            up_dt[idx]['keyword'] = r['keyword']
        line_num = line_num + 1
    of.close()
    # Close 201*.tsv


    # Write on 201*_issue.tsv or 201*_event.tsv
    of = open(file_path, 'w', newline="")
    tsv_writer = csv.DictWriter(of, delimiter='\t', fieldnames=headers)
    tsv_writer.writerow(dict((heads, heads) for heads in headers))
    tsv_writer.writerows(up_dt)
    of.close()
    # Close 201*_issue.tsv or 201*_event.tsv


def match_per_issue():
    for year in years:
        print(year, "tsv ......")

        file_path = "./hyeann/" + year + "_issue.tsv"
        up_dt = []

        # Read 201*_issue.tsv
        of = open(file_path, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        rep_docs_id = []
        for r in dt:
            row = {'representativedoc': r['representativedoc'],
                    'keyword': None,
                    'related1': r['related1'],
                    'related2': r['related2'],
                    'related3': r['related3'],
                    'related4': r['related4'],
                    'related5': r['related5']}

            rep_docs_id.append(int(r['representativedoc']))
            up_dt.append(row)
        of.close()
        # Close 201*_issue.tsv

        # Write KEYWORD on 201*_issue.tsv
        headers = ["representativedoc","keyword","related1","related2","related3","related4","related5"]
        match_keyword(year, rep_docs_id, up_dt, file_path, headers)

        print(year, "issue tsv completed\n")


def match_per_event():
    for year in years:
        print(year, "tsv ......")

        file_path = "./hyeann/" + year + "_event.tsv"
        up_dt = []

        # Read 201*_event.tsv
        of = open(file_path, 'r')
        dt = csv.DictReader(of, delimiter='\t')
        rep_docs_id = []
        for r in dt:
            row = { 'issue': r['issue'],
                    'event': r['event'],
                    'representativedoc': r['representativedoc'],
                    'keyword': None}

            rep_docs_id.append(int(r['representativedoc']))
            up_dt.append(row)
        of.close()
        # Close 201*_event.tsv

        # Write KEYWORD on 201*_event.tsv
        headers = ["issue","event","representativedoc","keyword"]
        match_keyword(year, rep_docs_id, up_dt, file_path, headers)

        print(year, "event tsv completed")


if __name__ == '__main__':
    match_per_issue()
    match_per_event()
