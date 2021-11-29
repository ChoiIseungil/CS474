from stanzaNER import ner
import csv

title = input("Enter the tile: ")
result = dict()

with open( './data/data.tsv','r') as f:
    reader = csv.reader(f,delimiter = '\t')
    for row in reader:
        if row[0]==title:
            tups = ner(row[1])
            for t in tups:
                if t[1] in result: result(t[1])+=t[0]
                else: result(t[1])=t[0]

print()

f.close()
