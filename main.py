# Written by Seungil Lee, Nov 30, 2021

import pandas as pd
import textwrap
from datetime import datetime
import ast

pd.options.display.max_colwidth = 200
pd.options.display.max_rows = 1000
preferredWidth = 100

input("""
Welcome to Korean Issue Tracker 2015-2017,
Developed by Seungil Lee, Yunho Lee and Hyeann Lee.

This is developed for a term project of the course: 2021 Fall CS474 Text Mining, instructed by Prof. Sung-Hyon Myaeng.
Please contact silly5921@kaist.ac.kr if you have any feedbacks.

Press Enter to continue.
Press Ctrl+C any time you want to exit.
    """
    )

for year in ["2015","2016","2017"]:
    issueDF = pd.read_csv("./data/" + year + "_issue.tsv", delimiter = '\t')
    ranking = issueDF["keyword"]
    ranking = ranking.to_string(index=False)
    ranking = ranking.split('\n')
    ranking = [r.split(',')[0].strip() for r in ranking]

    prefix = year + ": "
    wrapper = textwrap.TextWrapper(initial_indent = prefix, width=preferredWidth,
                                subsequent_indent=' '*len(prefix))
    message = ",".join(ranking)

    print(wrapper.fill(message))
    print()

while True:
    YEAR = input("""
         
Choose the year you want to investigate among 2015, 2016, 2017
    Input: """)

    if YEAR not in ['2015','2016','2017']:
        print("""
Only 2015, 2016, and 2017 are available
            """)

    else: break

issueDF = pd.read_csv("./data/"+ YEAR + "_issue.tsv", delimiter = '\t')

ranking = issueDF["keyword"]
ranking = ranking.to_string(index=False)
ranking = ranking.split('\n')
ranking = [r.split(',')[0].strip() for r in ranking]

summary = issueDF["summary"]
summary = summary.to_string(index=False)
summary = summary.split('\n')
summary = [s.strip("[] \"\'") for s in summary]

relateds = issueDF[["related1","related2","related3","related4","related5"]]

print(f"""
Top-10 Trending list for {YEAR} are as follows:
"""
)

for i in range(len(ranking)):
    print(f"""
[Top{i+1}]\t{ranking[i]}
[Summary]\t{summary[i]}""")



while True:
    ISSUE = input("""
         
Choose the issue you want to investigate among TOP10s
    Input: Top""")

    ISSUE = int(ISSUE)
    
    if ISSUE not in list(range(1,11)):
        print("""
    Input integer between 1 and 10
        """)

    else: break


ISSUE = ISSUE-1
issueKey = ranking[ISSUE]
issueSummary = summary[ISSUE]
issueRelateds = relateds.iloc[ISSUE].values.tolist()
issueRelateds = [int(i) for i in issueRelateds]


while True:
    MODE = input("""
         
Choose the mode
    1. On-issue Event Tracking
    2. Related-issue Event Tracking 
    Input: """)

    MODE = int(MODE)
    if MODE not in [1,2]:

        print("""
    Input is not valid, please check once again
        """)

    else: break


if MODE == 1:
    totalDF = pd.read_csv("./data/"+ YEAR + ".tsv", delimiter = '\t')
    dateDF = totalDF["date"]

    nerDF = pd.read_csv("./data/"+ YEAR + "_ner.tsv", delimiter = '\t')
    nerDF = nerDF["ner"]

    eventDF = pd.read_csv("./data/"+ YEAR + "_event.tsv", delimiter = '\t')
    eventDF = eventDF[eventDF['issue']==ISSUE]
    eventDF = eventDF[["representativedoc","keyword","summary"]]
    eventDF["keyword"] = eventDF["keyword"].apply(lambda s: s.split(',')[0])

    dateOrder = list()
    for doc in eventDF["representativedoc"]:
        dateOrder.append((doc, dateDF.iloc[doc], nerDF.iloc[doc]))

    dateOrder.sort(key=lambda date: datetime.strptime(date[1], "%m-%d"))
    
    eventSequence = list()

    for tup in dateOrder:
        doc = tup[0]
        row = eventDF[eventDF["representativedoc"]==doc]
        keyword = row["keyword"].to_string(index=False)
        eventSequence.append(keyword)
    
    print(f"""
[ISSUE]

{issueKey}
Summary: {issueSummary}



[On-Issue Events]

{" -> ".join(eventSequence)}



[Detailed Information (per event)]
    """
    )
    
    for tup in dateOrder:
        doc = tup[0]
        row = eventDF[eventDF["representativedoc"]==doc]
        keyword = row["keyword"].to_string(index=False)
        summary = row["summary"].to_string(index=False).strip("[] \"\'")
        nerDict = ast.literal_eval(tup[2])
        if not "PERSON" in nerDict: nerDict["PERSON"] = set()
        if not "ORG" in nerDict: nerDict["ORG"] = set()
        if not "LOC" in nerDict: nerDict["LOC"] = set()
        if not "GPE" in nerDict: nerDict["GPE"] = set()
        print(f"""

Event: {keyword}

Summary: {summary}
        
        - Person: {nerDict["PERSON"]}
        - Organization: {nerDict["ORG"]}
        - Place: {nerDict["LOC"] | nerDict["GPE"]}
        """)

    
elif MODE == 2:
    totalDF = pd.read_csv("./data/"+ YEAR + ".tsv", delimiter = '\t')
    totalDF = totalDF["keyword"]

    nerDF = pd.read_csv("./data/"+ YEAR + "_ner.tsv", delimiter = '\t')
    nerDF = nerDF["ner"]
    
    eventSequence = list()
    for i in issueRelateds:
        eventSequence.append(totalDF.iloc[i].split(',')[0])
    
    print(f"""
[ISSUE]

{issueKey}
Summary: {issueSummary}



[Related-Issue Events]

{",".join(eventSequence)}



[Detailed Information (per event)]"""
    )
    
    for i in issueRelateds:
        keyword = totalDF.iloc[i].split(',')[0]
        nerDict = nerDF.iloc[i]
        nerDict = ast.literal_eval(nerDict)
        if not "PERSON" in nerDict: nerDict["PERSON"] = set()
        if not "ORG" in nerDict: nerDict["ORG"] = set()
        if not "LOC" in nerDict: nerDict["LOC"] = set()
        if not "GPE" in nerDict: nerDict["GPE"] = set()
        print(f"""
Event: {keyword}

        - Person: {nerDict["PERSON"]}
        - Organization: {nerDict["ORG"]}
        - Place: {nerDict["LOC"] | nerDict["GPE"]}
        """)